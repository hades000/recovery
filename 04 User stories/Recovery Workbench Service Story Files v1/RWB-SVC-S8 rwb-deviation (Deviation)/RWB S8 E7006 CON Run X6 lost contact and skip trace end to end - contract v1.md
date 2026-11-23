# RWB-S8-E7006-CON Run X6 lost contact and skip trace end to end - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S8-E7006-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-deviation |
| Service epic | RWB-SVC-S8 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-006 |
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

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the X6 slice of rwb-deviation, split from RWB-E7-006. It fixes the X6 use of the `deviation` element and its DF-CAS fields, the three state values the trace writes, the skip-trace answer element consumed from rwb-agent, the internal contact data row consumed from rwb-source-data, the consumed rwb-case boundary, the two published events and their X6 payload, the rights, the fakes and the absence tests, on the base `/api/recovery/deviation/v1` (DP-13) behind the gateway-bff composite route (DP-19). It provides no operation of its own, because the two operations of the service were baselined at RWB-S8-E7001-CON and this story owns no new surface beyond them; the trace element, the consumed operation names, the agency read and the deviation service level have no published value, and TSD S8 T5.1 publishes no external interface for the bureau, the internal data or the agency (GAP-3062; ASM-5182 to ASM-5189). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the X6 lost contact and skip trace slice of rwb-deviation — the X6 use of the `deviation` element, the three state values the trace writes, the skip-trace answer element, the internal contact data row, the consumed rwb-case boundary, the two events with their X6 payload, the rights, the tables and the fakes**, so that **the app story, the screens and the agent and data-product owners build against one fixed, testable contract on Day 1, and a field, a state value, a consumed shape or a trace answer can never drift between rwb-deviation, rwb-case, rwb-source-data and rwb-agent without a failing build**.

The baseline is deliberately narrow: it declares one element's use, its X6 values and the boundaries the trace crosses. It declares no operation, no new event, no Schedule and no queue table of its own.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy X6 of RWB-E7-006 crossed four boundaries at once — a case state, a case timer, a bureau or agency answer and a decision log — inside one process and one schema. The target splits them: rwb-case owns the case, its route states and the timers; rwb-agent owns the skip trace and every source it works; rwb-source-data owns the internal contact data product; rwb-decision owns the rule package and the ledger; rwb-deviation owns the deviation row and the record. Each boundary is a contract another team builds against, so each has to be fixed before the app story starts.

The baseline also fixes the naming the checks require: schema `rwb_deviation`, login `rwb_deviation`, base `/api/recovery/deviation/v1`, topic `rwb.deviation.events.v1` with its retry and `.dlt` topics, task queue `rwb-deviation` in namespace `rwb-recovery`, the agent's queue `rwb-agent`, and Java package `th.co.scb.ace.workbench.recovery.deviation` (Template and Rules v1 §R4; context pack service row). It records that rwb-deviation holds no grant on `rwb_case`, `rwb_agent`, `rwb_source_data` or `rwb_partner`, so all four are consumed on their owners' contracts only.

Four points are carried as gaps and assumptions rather than decided quietly: the skip-trace answer element and every consumed operation name are unpublished (GAP-3062; ASM-5182, ASM-5183), the bureau and agency sources have no interface at all and no matrix row (ASM-5184), the 30-day clock and the 10-working-day escalation are workflow timers and not Schedules (ASM-5186), and the two events are the service's while the plan's pattern set carries neither DP-09 nor DP-14 (ASM-5185).

The wave and the date are the plan's and the legacy epic's: this key is EP07, wave 4, release 31 May 2027, while rwb-deviation is created in service wave 2, so the two do not agree and the plan's wave stands with the date copied unchanged and marked tentative (ASM-5187).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queues and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline; where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the context pack and the Ownership Map only: `deviation` is S8's, `recovery_case`, `assignment` and `timer` are P3's, `rule_row` and `decision_log_entry` are P7's, `partner` is S9's, the contact data product is P1's and the trace is P10's. This document never declares another service's table or operation as its own.
- The two operations of this service, `POST /cases/{caseId}/deviations` (API-S8-001) and `PATCH /deviations/{deviationId}` (API-S8-002), were baselined at RWB-S8-E7001-CON; this baseline fixes the X6 use of their elements and declares no new one (ASM-5188).
- The rwb-case boundary, the rwb-agent trace and the rwb-source-data contact row are published with their fakes, so each consumed row names a real owner document; they are not in this story's dependency rows, which are None, and the absence is recorded (GAP-3062; ASM-5182, ASM-5183, ASM-5184).
- The DEV rule package and its rows for R-DEV-01, R-DEV-06, R-DEV-16, R-DEV-17, R-DEV-18, R-DEV-19, R-DEV-20 and R-UNI-12 are governed in rwb-decision (P7); this baseline names them and declares none of them.
- The `deviation` table and its columns arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- The deviation service level that R-DEV-20 escalates against is set with DL22 and has no published value; it is declared as reference data with a placeholder and never as a default (GAP-3062; ASM-5189).
- No build dependency: this story is Day 1 by rule (Template and Rules v1 §R5.7).

### 4. Flow

1. Draft the additive document of rwb-deviation for this slice and record that it declares no operation of its own, naming the two operations of the service and their owner baseline.
2. Fix the X6 use of the `deviation` element: the properties of DF-CAS-036 to DF-CAS-045 with their types, lengths, required flags and lists, and the values X6 writes.
3. Fix the three state values the trace writes — `DEV_WITH_OWNER`, `DEV_RESOLVED` and `DEV_REROUTE` — against the DEVIATION vocabulary already published at the service baseline, and record that FSD S8 A2.15.3.1 prints no rule row for this feature.
4. Fix the consumed rwb-case boundary: the case state, the `paused_state`, the stage and prescription clocks and the stage outcome, with the placeholder on every name the sources do not publish.
5. Fix the consumed rwb-agent trace element: the request, the answer and the source codes, and record that no source publishes its shape (ASM-5183).
6. Fix the consumed rwb-source-data contact-data row and its freshness stamp, and record that the bureau and agency sources have no interface and no matrix row (ASM-5184).
7. Fix the two published events and their X6 payload, and record that DP-09 and DP-14 are not in the plan's pattern set (ASM-5185).
8. Record the decision-record element of DP-03, written before the `deviation` row changes, and the 30-day and 10-working-day waits as workflow timers rather than Schedules (ASM-5186).
9. Publish the contract tables of section 12, the rights and the fakes of 12.8.
10. Add the contract tests: schema validation, the additive rule, the vocabulary, the element shapes, the error set, the rights, the drift between a fake and the document, the absence of a new operation, of a new event, of a Schedule and of a foreign table.
11. Tag the baseline and hand it to RWB-S8-E7006-APP, the two screen fragments and the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A body fails schema validation, or an element carries a value outside the state vocabulary | The build fails on the schema and vocabulary lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC2, AC7 |
| X2 | A field is renamed or removed within major version 1, or a state value changes | The contract test fails; the change needs a new major version | None | AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a field list or a name the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC3, AC4 |
| X5 | The document declares a new operation, a new event, a Schedule, a queue table or another service's object as its own | The absence test and the boundary test fail the build | None | AC1, AC7 |
| X6 | The rights of the operations and of the consumed acts are not the ones TSD S8 T6.1 and T-A.1 declare, or the unattended and agent identities are given a user right | The access test fails the build | MSG-P4-002 | AC5 |
| X7 | A trace window, a service level or a contact point is declared with a value no source gives, or as a schema default | The review fails the baseline; the element carries the placeholder | None | AC2, AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack and the published owner contracts of rwb-case, rwb-source-data and rwb-agent only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the fields, the state values, the base, the topic and the queues are fixed by the target architecture |
| Valuable | Unblocks RWB-S8-E7006-APP, the two screen fragments and the wave 4 harness on Day 1, and the rwb-agent and rwb-source-data teams on the same day |
| Estimable | One additive document, nine contract tables, seven fakes and seven new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the X6 lost contact and skip trace slice of rwb-deviation

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of deviation is S8, of recovery_case and timer is P3, of partner is S9, of rule_row and decision_log_entry is P7, of the trace is P10 and of the contact data product is P1
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The baseline provides no operation of its own and records the service's two operations and its two events as already baselined (new, D-RCV-60)
    Given the additive document of rwb-deviation is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares no operation whose behaviour is the X6 lost contact and skip trace flow
    Then it records POST /cases/{caseId}/deviations (API-S8-001) and PATCH /deviations/{deviationId} (API-S8-002) as the service's, baselined at RWB-S8-E7001-CON, with the error set of 400, 401, 403 with MSG-P4-002, 404, 409, 422 with MSG-GEN-001 and 503 and one message ID per condition
    Then it declares no event beyond DeviationRaised (EV-06) and DeviationCleared (EV-07) (ASM-5185)
    Then the absence test fails a build that declares a new operation, a third event, a second base or a second topic

  Scenario: AC2 The X6 use of the deviation element and the three state values are declared (new, D-RCV-60)
    Given the deviation section of the baseline
    When it is compared with TSD S8 T3.0, T3.1, T3.2 and T4 and with the element published at RWB-S8-E7001-CON
    Then the element declares the properties of DF-CAS-036 to DF-CAS-045: id, case_id, deviation_code, raised_at, raised_by, paused_state, handler_user_id, contact_stop, cleared_at and outcome
    Then case_id, deviation_code, raised_at, raised_by, paused_state and contact_stop are required, deviation_code is a varchar(3) of LOV-DEVIATION carrying X6, raised_by is a varchar(20) of LOV-RAISED-BY and outcome is of LOV-DEV-OUTCOME
    Then state is declared against the DEVIATION vocabulary, and the trace writes DEV_WITH_OWNER, DEV_RESOLVED and DEV_REROUTE and no other value
    Then the element records that FSD S8 A2.15.3.1 prints VR-S8-015-1 and BR-S8-015 and no rule row, that the rules are taken from Business Rules and Routing Logic v4 under GAP-3062, and that the 30-day window of R-DEV-17 and the deviation service level are reference data with a version and Not specified in the source documents (GAP-3062; ASM-5186, ASM-5189)

  Scenario: AC3 The consumed rwb-case boundary is declared and no case or timer property is declared (new, D-RCV-60)
    Given the consumed rows and the case boundary of the baseline
    When they are compared with rwb-case as the owner of recovery_case, assignment and timer
    Then the case state read is declared as consumed with the case reference, the route state and the paused_state, and its operation name is Not specified in the source documents (GAP-3062; ASM-5182)
    Then the stage outcome is declared as the child-workflow result carrying the rule ID, its version, the return point and CLOCK_PAUSE, CLOCK_RESUME or ROUTE_D6, and it moves no case state of its own
    Then the stage clock and the prescription clock are declared as consumed and as the parent's, with the timer item of DF-WRK-027 to DF-WRK-036, and their names are Not specified in the source documents (GAP-3062; ASM-5182)
    Then the document declares no recovery_case property, no assignment property, no timer property and no write of a case or timer row from rwb-deviation, and records that the connection matrix gives S8 events from P3 and no REST edge

  Scenario: AC4 The consumed rwb-agent trace and the rwb-source-data contact row are declared (new, D-RCV-60)
    Given the consumed rows of the trace and of the internal contact data
    When they are compared with rwb-agent as the owner of the trace and with rwb-source-data as the owner of the contact data product
    Then the trace request and answer are declared as consumed from P10 rwb-agent on its queue, with the case reference, the deviation reference, the trace window, the source of each contact point and the verified flag, and their names and element are Not specified in the source documents (GAP-3062; ASM-5183)
    Then the contact data read is declared as consumed from P1 rwb-source-data with the data product and its freshness stamp, and its operation name is Not specified in the source documents (GAP-3062; ASM-5184)
    Then the bureau (NCB) and agency (Partner portal) answers are declared as consumed inside the trace answer with a placeholder, and the document records that TSD S8 T5.1 publishes None, that the matrix gives S8 no row to P2 or S9 and that the partner row of DF-PRT-001 to DF-PRT-007 is never declared as this service's (GAP-3062; ASM-5184)
    Then each consumed row is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC5 The rights, the roles and the unattended and agent identities are fixed (new, D-RCV-60)
    Given the access section of the baseline
    When it is compared with TSD S8 T6.1 and T-A.1 and with the legacy permission rows
    Then the two operations declare Case record right U with the scope applied, and RW-CASEOWN holds CRU while RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE and RW-SALEOFF hold RU
    Then the document records that FSD S8 A2.15.3.3 names no primary role, that the case owner is a secondary user and that X6 runs unattended under the service identity
    Then the document records that the agent works the trace under R-DEV-06 and is subject to the same role checks as a person (NFR-051), and it declares no A right on any operation
    Then a build that gives the unattended or agent identity a user right fails the access test

  Scenario: AC6 The decision-record element, the two events and the fakes answer the document (new, D-RCV-60)
    Given the entry section, the event section and the fakes of the baseline
    When each is compared with the library schema, with the service's event catalogue and with the element it serves
    Then one decision record is declared per raise, per routing and per outcome, with the case reference, the deviation reference, the rule ID, the package version in force, the inputs reference and the state
    Then the record is written through the library on the shared rwb.decision-record.v1 before the deviation row changes, and a failed write leaves the row unchanged with MSG-P7-003
    Then DeviationRaised (EV-06) and DeviationCleared (EV-07) are declared on rwb.deviation.events.v1 with their X6 payload, no personal data and no new event or producer group
    Then the rwb-case fake answers the case state, the paused_state, the three outcomes and a refused outcome, the rwb-agent fake answers a verified contact point from each of the three sources, an exhausted trace and a late answer, and the rwb-source-data fake answers a fresh and a stale stamp
    Then the trace element, the consumed operation names, the agency read and the deviation service level carry the placeholder (GAP-3062; ASM-5183, ASM-5184, ASM-5189)
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline and the boundary are fixed and nothing is scheduled (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the context pack and the Ownership Map, with None where the element is empty
    Then the schema is rwb_deviation, the login is rwb_deviation, the base is /api/recovery/deviation/v1, the topic is rwb.deviation.events.v1, the queue is rwb-deviation, the agent's queue is rwb-agent and the Java package is th.co.scb.ace.workbench.recovery.deviation
    Then the tables named as owned are deviation and the library objects decision_record, idempotency_key and outbox_event, and recovery_case, assignment, timer, partner, rule_row, decision_log_entry, the contact data product, the trace and every v_ace_* view are named as other owners' and are consumed only through their contracts
    Then the document declares no Schedule, no Quartz row, no shared job table and no batch table, records that the 30 days of R-DEV-17 and the 10 working days of R-DEV-20 are durable timers of the workflow, and names no job of this service because the Ownership Map gives S8 none (ASM-5186)
    Then the document records that the plan's C and I rows are empty although the slice consumes three services, and that the S8 module files were read from the extract folder (GAP-3062; ASM-5182)
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S8-E7006-APP and they copy no criterion of the legacy story, whose one criterion in this split stays with the app story word for word.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The `deviation` row and its state are rwb-deviation's, and the contract declares their fields and the three X6 values on that element only | Context pack ownership row `deviation`; TSD S8 T3.0 and T3.1; DP-01 |
| BR2 | The decision record is declared as an element written before the row changes, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S8 T2; legacy RWB-E7-006 AC2 |
| BR3 | The case, its route state and the two clocks stay with rwb-case: the contract declares the state, the paused_state, the outcome and the timer rows as consumed and declares no `recovery_case`, `assignment` or `timer` property | Context pack connection matrix row S8; ASM-5182 |
| BR4 | The trace and every source it works stay with rwb-agent: the contract declares the request and the answer as consumed, declares no bureau, agency or model detail, and records that TSD S8 T5.1 publishes no external interface | TSD S8 T5.1; context pack connection matrix row S8; ASM-5183, ASM-5184 |
| BR5 | The internal contact data product stays with rwb-source-data: the contract declares the read and its freshness stamp as consumed and declares no view and no table of its own | FSD S8 A2.15.3.1; context pack connection matrix row S8; ASM-5184 |
| BR6 | The partner and agency record stays with its owner: the contract declares the agency answer inside the trace with a placeholder and declares no partner property | Legacy Data table (`partner`, DF-PRT-001 to DF-PRT-007); ASM-5184 |
| BR7 | The two events are the service's and the baseline adds none: `DeviationRaised` (EV-06) and `DeviationCleared` (EV-07) on `rwb.deviation.events.v1`, with their X6 payload and no personal data | Context pack topic and ownership rows; TSD S8 T5.3; ASM-5185 |
| BR8 | No Schedule belongs to this slice: the 30-day window and the 10-working-day escalation are durable timers of the workflow, and the Ownership Map gives S8 no job | Business Rules and Routing Logic v4 rows R-DEV-17 and R-DEV-20; ASM-5186 |
| BR9 | The state vocabulary is closed: the three values are published against the DEVIATION enumeration the service baseline already declares, and no state value is a constant of the code | TSD S8 T3.0 and T4 |
| BR10 | No personal data in a schema, an example or a fake: identifiers, a code, a source code, an instant and a rule version only | Template and Rules v1 §R7.2 s17 |
| BR11 | One REST base, one topic, two queues and one login per service; the document never declares another service's base, topic or queue as its own | DP-13; Template and Rules v1 §R4 |
| BR12 | A schema change is additive within major version 1; a breaking change is a new major version | Architecture v5 slide 11 notes (BACKWARD compatibility) |
| BR13 | The document declares no operation of its own: the two operations are the service's and were baselined at RWB-S8-E7001-CON, so a consumed element is described as consumed and faked, never as provided | Ownership rows; DP-11; ASM-5188 |
| BR14 | No window, no service level and no contact point is a schema default or a constant: the window and the service level are reference data with a version and the contact point is a reference | FSD S8 BR-S8-015; ASM-5186, ASM-5189 |

### 9. State transitions

The lifecycle of this document, not of a deviation:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The element use, the three state values, the consumed rows, the events and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the two screen fragments, the wave 4 harness and the rwb-case, rwb-source-data and rwb-agent owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property or a payload field is added within major version 1 | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a state value changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence and boundary tests of AC1 and AC7 fail: a new operation, a third event, a Schedule, a queue table or a foreign table | In review |

The DEVIATION machine the document describes is the app story's: `DEV_WITH_OWNER`, `DEV_RESOLVED` and `DEV_REROUTE` are the values the trace reads and writes, and the case route state that rwb-case holds is answered, not declared here. This baseline fixes the vocabulary and moves no deviation and no case.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-deviation | Owns the additive document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the consumed rows |
| Consuming teams (the app story, the two screen fragments, the wave 4 harness and the owners of rwb-case, rwb-source-data and rwb-agent) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake |
| Compliance and Legal | Confirm the deviation service level and the trace window the element names as reference data, which are open under DL22 |

The per-service login behind the security scheme of the document is named "the rwb-deviation login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Deviation element, X6 use | The columns of DF-CAS-036 to DF-CAS-045: `id`, `case_id`, `deviation_code`, `raised_at`, `raised_by`, `paused_state`, `handler_user_id`, `contact_stop`, `cleared_at`, `outcome` |
| Required flags | `case_id`, `deviation_code`, `raised_at`, `raised_by`, `paused_state` and `contact_stop` required; `handler_user_id`, `cleared_at` and `outcome` optional, as TSD S8 T3.1 declares them |
| Lists | `LOV-DEVIATION` with X1 to X7 and X6 the value here, `LOV-RAISED-BY` with SCREENING_AGENT, RULE, OFFICER and CUSTOMER_CONTACT, `LOV-DEV-OUTCOME` with RETURNED, RE_ROUTED and CASE_ENDED |
| State | `state` of TSD S8 T3.0 against the DEVIATION vocabulary; the trace declares `DEV_WITH_OWNER`, `DEV_RESOLVED` and `DEV_REROUTE` and no other |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the row changes (DP-03) |
| Trace element | The request and the answer of rwb-agent: the case reference, the deviation reference, the trace window, the source of each contact point and the verified flag; Not specified in the source documents (GAP-3062; ASM-5183) |
| Contact data | The internal contact data product and its freshness stamp of P1, declared as consumed; its operation name is Not specified in the source documents (GAP-3062; ASM-5184) |
| Not declared here | `recovery_case`, `assignment` and `timer` (P3), `partner` (S9), `rule_row` and `decision_log_entry` (P7), the bureau and agency interfaces (None in TSD S8 T5.1), every `v_ace_*` view (P1) |
| Values with no source | The trace window, the deviation service level and the agency answer: Not specified in the source documents (GAP-3062; ASM-5186, ASM-5189) |

The field-level formats of the added elements are settled in the baseline review; this story fixes the element names, the three state values of AC2 and the optionality rule of BR12. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

None of its own. Owner rwb-deviation (S8); base `/api/recovery/deviation/v1` (DP-13). The two operations of this service — `POST /cases/{caseId}/deviations` (API-S8-001, Case record right U) and `PATCH /deviations/{deviationId}` (API-S8-002, Case record right U) — were baselined at RWB-S8-E7001-CON and are the only surface X6 uses; this baseline fixes the X6 use of their elements and declares no additional operation, no additional base and no additional topic. A build that declares an X6 operation here fails the absence test of AC1 (ASM-5188).

#### 12.2 REST operations consumed

| Method and path | Owner | Use in the baseline |
|---|---|---|
| The case state, paused_state and timer read (operation name Not specified in the source documents (GAP-3062; ASM-5182)) | P3 rwb-case | The case, its route state, its `paused_state`, the stage clock and the prescription clock of the timer item of DF-WRK-027 to DF-WRK-036; consumed on the workflow boundary and the case events, because the matrix gives S8 events from P3 and no REST edge; faked |
| The stage outcome (operation name Not specified in the source documents (GAP-3062; ASM-5182)) | P3 rwb-case | `CLOCK_PAUSE`, `CLOCK_RESUME` or `ROUTE_D6` with the rule ID, its version and the return point; on the workflow boundary it is the child result the parent `CaseWorkflow` applies; faked |
| The skip-trace request and answer (element and operation Not specified in the source documents (GAP-3062; ASM-5183)) | P10 rwb-agent | The trace on rwb-agent's queue: the case reference, the deviation reference, the window, the source of each contact point and the verified flag; the rwb-agent contract of DP-20 applies and DP-20 is not in the plan's pattern set; faked |
| The internal contact data read (operation name Not specified in the source documents (GAP-3062; ASM-5184)) | P1 rwb-source-data | The contact data product of the case and its freshness stamp; the one REST edge the matrix gives S8; faked |
| The agency answer (operation and owner Not specified in the source documents (GAP-3062; ASM-5184)) | S9 rwb-partner, or the agency's own interface | Not reachable: TSD S8 T5.1 publishes None and the matrix gives S8 no row to S9 or to P2; the answer is declared as arriving inside the trace answer with the placeholder; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). Only the contact data read is a REST row of the connection matrix; the others are the workflow boundary, the agent activity and a read no source publishes. The five rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded as GAP-3062 with ASM-5182, ASM-5183 and ASM-5184.

#### 12.3 Events published

| Event | Topic | X6 payload this baseline fixes |
|---|---|---|
| `DeviationRaised` (EV-06, `rwb.deviation.DeviationRaised.v1`) | `rwb.deviation.events.v1`, with `.retry` and `.dlt` | Case reference, deviation reference, code X6, raised-at, paused state, contact-stop flag, rule ID and version; CloudEvents envelope; no personal data |
| `DeviationCleared` (EV-07, `rwb.deviation.DeviationCleared.v1`) | `rwb.deviation.events.v1`, with `.retry` and `.dlt` | Case reference, deviation reference, outcome (`CONTACT_RESTORED` or `CONTACT_NOT_FOUND`), the source code of the contact point, cleared-at, rule ID and version; CloudEvents envelope; no personal data |

The two events are the service's and were declared at the service baseline; this baseline fixes their X6 payload and adds no producer, no third event and no outbox row of its own, and the absence test of AC1 fails a build that adds one (ASM-5185). DP-09 and DP-14 are not in the plan's pattern set although the outbox library and the topic naming rule are both needed; they are recorded as absent rather than added (ASM-5185).

#### 12.4 Events consumed

| Event | Owner | Use in the baseline |
|---|---|---|
| The case events of rwb-case; event names Not specified in the source documents (GAP-3062; ASM-5182) | P3 rwb-case | The case move that keeps an open X6 aligned with its case and the contact change that raises R-UNI-12; the consumer group is declared against the placeholder and faked |

The S8 row of the connection matrix names an event subscription to P3 and none of its event names is published, so the baseline declares the subscription and no name. This baseline declares no other consumer group, no other subscription and no other inbox row, and the absence test of AC7 fails a build that adds one (ASM-5182).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DeviationWorkflow` | Workflow, one execution per case, the always-on child of `CaseWorkflow` | `rwb-deviation` in namespace `rwb-recovery` | The stage that hosts the X6 branch; its input, its signals and its outcome for the parent are declared, not built |
| The X6 branch of `DeviationWorkflow` | Workflow branch | `rwb-deviation` | The step from the raise to the verified point or the exhausted trace: R-DEV-01, R-DEV-06, the trace, R-DEV-16 or R-DEV-17, R-DEV-18 or R-DEV-19, the record, the row and the stage outcome |
| `runSkipTrace` | Activity dispatched to the owner's queue | `rwb-agent` | The request in; the source of each contact point and the verified flag out (ASM-5183) |
| `readContactData` | Activity | `rwb-deviation` | The case reference in; the contact data product and its freshness stamp out (ASM-5184) |
| `recordAndApplyDeviation`, `resolveDeviation` | Activities, the RecordAndApply step and the outcome step | `rwb-deviation` | The decision in; the row, the outbox rows and the stage outcome out, written before the answer |
| `traceClock` | Durable timer | `rwb-deviation` | The 30 days of R-DEV-17 from the reference data with its version; the expiry is `CONTACT_NOT_FOUND` (ASM-5186) |

No child workflow of this service exists in this slice and no timer table is declared here: the `timer` rows are P3's and are changed on its contract. The activity and branch names are target design choices and no source document fixes them; no activity is registered by this story.

#### 12.6 Schedules

None. The 30 days of R-DEV-17 and the 10 working days of R-DEV-20 are durable timers inside `DeviationWorkflow`, so this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table, and the Ownership Map gives S8 no job at all. DP-10 is not in this key's pattern set (ASM-5186).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| deviation | S8 (`rwb_deviation`) | The X6 record: its DF-CAS fields, its `state`, its `contact_stop` and its `outcome`; the table the element answers from |
| decision_record | PLT library, created in `rwb_deviation` | The local hash-linked record of DP-03 |
| idempotency_key | PLT library, created in `rwb_deviation` | The raise and advance keys and the answers they hold |
| outbox_event | PLT library, created in `rwb_deviation` | Created in this schema by the library for the two events; no row of it is added by this baseline |

`recovery_case`, `assignment` and `timer` (P3), `partner` (S9), `rule_row` and `decision_log_entry` (P7), the contact data product (P1), the trace (P10) and every `v_ace_*` view (P1) are not owned by this baseline; it names them only as answers, rule versions or records of their owners, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case state and outcome fake | The states of case `RW-2027-001206` with its `paused_state`; `CLOCK_PAUSE`, `CLOCK_RESUME` and `ROUTE_D6` accepted and one refused; no answer beyond 2 s | AC3, AC6 |
| rwb-agent trace fake | A verified contact point from the bureau, from the internal data and from the agency, an exhausted trace, and an answer that does not arrive inside its budget; the element carries the placeholder (GAP-3062; ASM-5183) | AC4, AC6 |
| rwb-source-data contact fake | The contact data product with a fresh stamp and with a stale stamp | AC4, AC6 |
| Agency answer fake | An agency contact point inside the trace answer, and an agency answer with no verified point; the read carries the placeholder (GAP-3062; ASM-5184) | AC4, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain, and a stopped chain | AC6 |
| rwb-deviation deviation fake | `DEV-2027-001206` of code X6 on case `RW-2027-001206` in `DEV_WITH_OWNER`, `DEV_RESOLVED` and `DEV_REROUTE`, with its handler, its contact stop and its outcome | AC2, AC6 |
| gateway-bff composite route fake | The merged SCR-08 and SCR-06 answer for the deviation, with the deviation facts of this service read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The trace element, the consumed operation names, the agency read and the service level are derived from the published documents and carry the placeholder until their owners confirm them (GAP-3062; ASM-5182, ASM-5183, ASM-5184, ASM-5189).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 1 consumed | The rwb-source-data contact data read; one hop, 2 s. The two operations the slice uses are the service's and are provided by the service baseline, not by this document |
| Kafka | 2 published, 1 consumed | `DeviationRaised` (EV-06) and `DeviationCleared` (EV-07) with their X6 payload; the rwb-case case events; the decision record is the library's on `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 1 workflow, 1 branch, 4 activities declared, 1 dispatched activity and 1 durable timer | `DeviationWorkflow` and its X6 branch on `rwb-deviation`, with `runSkipTrace` on `rwb-agent`, `readContactData`, `recordAndApplyDeviation` and `resolveDeviation`, and the 30-day `traceClock`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no deviation, no case and no rule package. What it publishes is one additive document, nine contract tables, the rights of the two operations and seven fakes.

**Deliverables.** The additive document `openapi/rwb-deviation-v1.yaml` with the X6 section and the trace element, the contract README rows for the five consumed rows and their placeholders, and the seven WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H `RWB-PLT-E1027-CON` |
| DP-13 | `/api/recovery/v1` | `/api/recovery/deviation/v1` | None |
| DP-19 | Screen, ace-web | gateway-bff composite route | H `RWB-PLT-N001-CON` |

DP-03 is the element the baseline declares before the row changes, on the shared `rwb.decision-record.v1`. DP-13 fixes the base of the two operations and adds none, because this document owns no operation. DP-19 is behind SCR-08 and SCR-06, whose screen model is the edge contract's, and this baseline fixes the deviation answer only. No other pattern is claimed: the case, the contact data, the trace and the agency are consumed contracts, so DP-04, DP-05, DP-09, DP-14 and DP-20 stay off this table and their absence is recorded in the registers (GAP-3062; ASM-5183, ASM-5184, ASM-5185).

**Build steps**

1. Record that this document declares no operation of its own and names the two operations of the service and their owner baseline, with the absent-operation test of AC1.
2. Write the X6 section of the `deviation` element, its required flags, its lists and the three state values of AC2, with the unprinted rule rows and the window placeholder.
3. Record the rwb-case rows of AC3 with their owner, their budget and the placeholder.
4. Record the rwb-agent trace element and the rwb-source-data contact row of AC4 with their owners, and the agency answer with its placeholder.
5. Record the rights, the roles and the unattended and agent identities of AC5.
6. Record the decision-record element of AC6 and the two events with their X6 payload, validate both against the library schema and the event catalogue, and publish the seven fakes with the drift test.
7. Record the naming baseline and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

**Done when.** The document validates in the pipeline, the seven contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, the two screen fragments and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S8-001 | The raise succeeds and the case moves to its handler; carried from the legacy message set of this key and raised by the behaviour, not by the contract | {deviation} was raised. The case is with {handler}. |
| MSG-GEN-001 | A required field of a body is absent or invalid, a body fails schema validation, or a window has no version in force | Enter {field}. |
| MSG-P4-002 | The role lacks the Case record right the operations declare, and a role without the right of a consumed act tries it | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the deviation row changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The contact data product is stale when the trace answer is read | {product} is from {date}. Today's ACE batch has not arrived. |

The five IDs are those of the legacy and FSD message set of this key; the text is the legacy and FSD S8 wording, copied unchanged, and no message is reworded or added. The deviation service level behind R-DEV-20 is set with DL22 and has no published value (ASM-5189).

### 15. Screens and states

The contract serves SCR-08 Deviation queue and SCR-06 Raise deviation, through the gateway-bff composite route (DP-19). The route calls rwb-deviation for the deviation, its state and its outcome, rwb-case for the case, its route state and its timers, and rwb-agent for the trace status; this baseline fixes the rwb-deviation answer only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The trace status behind the list is a placeholder on its element, because no source publishes it (ASM-5183). The legacy screen table's two states, form and saved, and loading and list, are the app story's; the refused, not-recorded, exhausted and stale-data states read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-006-01 | AC1, AC2 | Contract | The synthetic case `RW-2027-001206`; the contract half answers the X6 element, its state and the absent new operation |
| TC-E7-006-02 | AC2, AC6 | Contract | An X6 in `DEV_WITH_OWNER`; the contract half answers the record element and the MSG-P7-003 path |
| TC-E7-006-03 | AC5 | Contract | A role without the Case record right; the contract half answers the 403 with MSG-P4-002, the rights and the unattended identity |
| TC-E7-006-04 | AC6, AC7 | Contract | A forced record failure and a forbidden element; the contract half answers the record path and the absence tests |
| TC-S8-E7006-CON-01 | AC1 | Contract | The document validates; no X6 operation, no third event, no second base and no second topic are declared, and the two operations of the service are named with their owner baseline |
| TC-S8-E7006-CON-02 | AC2 | Contract | The X6 element validates with its ten properties, its six required flags, the three lists and the three state values against the published enumeration |
| TC-S8-E7006-CON-03 | AC3 | Contract | The case state, the paused_state, the outcome and the timer rows with their placeholders; the no-`recovery_case`, no-`assignment` and no-`timer` boundary |
| TC-S8-E7006-CON-04 | AC4 | Contract | The trace element, the contact data row and the agency answer with their placeholders; no partner property and no external interface |
| TC-S8-E7006-CON-05 | AC5 | Contract | RW-CASEOWN holds CRU, the seven read and update roles hold RU, and the unattended and agent identities hold no user right |
| TC-S8-E7006-CON-06 | AC6 | Contract | The seven fakes match the document, the two events carry their X6 payload, and a drifted fake fails the build |
| TC-S8-E7006-CON-07 | AC7 | Contract | The naming baseline; the absence test for a Schedule, a Quartz row and a shared job table, and the boundary test for a `v_ace_*` path and a foreign table property |

The four legacy cases are the legacy cases of RWB-E7-006 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S8-E7006-APP. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The seven cases `TC-S8-E7006-CON-01` to `-07` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 4 harness and are not written here.

### 17. Guardrails

- No business value in the contract: the trace window, the deviation service level, the state values and the rule rows stay reference data or an enumeration, never a schema default or a constant of the code.
- No personal data in a schema, an example or a fake: identifiers, a code, a source code, an instant and a rule version only, and every example is synthetic.
- The case and the clocks stay with rwb-case, the trace with rwb-agent, the contact data with rwb-source-data and the agency record with its owner: the document declares no `recovery_case`, `assignment`, `timer`, `partner` or view property and no row write of any of them (BR3, BR4, BR5, BR6).
- The document owns no operation of its own and adds no event: the absence tests fail a build that declares one (BR7, BR13).
- One base, one topic, two queues and one login per service; a document that names another service's base, topic or queue as its own fails the review (DP-13).
- No retired element is reintroduced: the absence tests fail a build that declares a Schedule, a Quartz row, a shared job table or a direct bureau or agency interface (BR4, BR8).
- The window is never a default: a window or a service level with no version in force is refused at the boundary (X7, BR14).
- The error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S8-004 | A lost contact case runs skip tracing and returns to a decision whether or not contact is restored (Must, E7) | The X6 use of `deviation`, the three state values, the trace element, the contact row and the two events | TC-E7-006-01, TC-E7-006-02, TC-S8-E7006-CON-02, TC-S8-E7006-CON-04 |
| REQ-DVH-011 | The full deviation flows with their approvers, contact stops and return points run end to end (Must, E7) | The consumed rwb-case boundary, the return point and the stage outcome | TC-S8-E7006-CON-03 |
| ADR-014 | Schema and login per service | `rwb_deviation` and its own login | TC-S8-E7006-CON-07 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The consumed rows with their budget and breaker | TC-S8-E7006-CON-03, TC-S8-E7006-CON-04 |
| ADR-022 | Local decision record plus central ledger | The record element and the ledger entry of P7 | TC-S8-E7006-CON-06 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E7-006, disposition Split (rework); feature FEAT-DVF-06 |
| Legacy criteria | AC1 of the legacy story is owned by RWB-ITG-E7006-ITG; AC2 is owned word for word by RWB-S8-E7006-APP, and this baseline copies none of them |
| Test cases | The four legacy cases as the contract half, and the seven new contract cases TC-S8-E7006-CON-01 to -07 |
| Feature and screens | FEAT-DVF-06, SCR-08 Deviation queue and SCR-06 Raise deviation |
| Rules | R-DEV-01, R-DEV-06, R-DEV-16, R-DEV-17, R-DEV-18, R-DEV-19, R-DEV-20 and R-UNI-12, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-014 (schema and login per service), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the element use: the evaluation of R-DEV-01, R-DEV-06, R-DEV-16, R-DEV-17, R-DEV-18, R-DEV-19, R-DEV-20 and R-UNI-12, the state write, the record, the trace dispatch and the stage outcome: RWB-S8-E7006-APP.
- The end-to-end X6 journey across the services and the run report: RWB-ITG-E7006-ITG.
- The other six codes and their flows (X1 to X5, X7), the screening agent and its policy, the low-confidence review, two deviations on one case, the contact-breach path, the override review and the complaint-to-contact matching: each is its own story of this service.
- The case of record, its route state, its assignment, its queues and its timers: rwb-case (P3), whose answers this baseline declares as consumed and faked.
- The skip trace itself, its policy and its model, and the bureau, internal data and agency connections: rwb-agent (P10); the internal contact data product: rwb-source-data (P1).
- The agency and partner record, its panel, its contract and its SLA: S9 rwb-partner, which no interface of this baseline reaches.
- The DEV package and the ledger: rwb-decision (P7); the roles and the reference data: rwb-access (P4).
- The schema and migration of `rwb_deviation`, the login, the deployment, the observability, the alerts and the runbook: the DB, INF and OPS stories of this legacy key.
- Any change to a legacy file, to a master or to built Epic 1 and Epic 2 code.

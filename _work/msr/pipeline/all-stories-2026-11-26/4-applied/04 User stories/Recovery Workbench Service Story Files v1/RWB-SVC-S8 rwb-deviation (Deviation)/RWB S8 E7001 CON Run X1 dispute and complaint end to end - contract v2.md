# RWB-S8-E7001-CON Run X1 dispute and complaint end to end — contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S8-E7001-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-deviation |
| Service epic | RWB-SVC-S8 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-001 |
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

**Change log.** D-RCV-60, 22 November 2026: the contract baseline of RWB-E7-001 for rwb-deviation (S8, service wave 2, business wave 4) is published as its own story so the app slice can build on Day 1. The baseline fixes the two write operations on `/api/recovery/deviation/v1` (DP-13), the `deviation` element with the fields of DF-CAS-036 to DF-CAS-045 and the three closed lists, the `DeviationRaised` and `DeviationCleared` envelopes on `rwb.deviation.events.v1`, the consumed document and data-product rows, the case workflow boundary, the decision-record element of DP-03, the error set and the seven fakes. It declares no `v_ace_*` property, no `recovery_case` property and no queue read. The pairing of the two event ids, the operation names of the two consumed reads and the error message per status are placeholders because no source publishes them (GAP-3052; ASM-5134, ASM-5137, ASM-5138, ASM-5139, ASM-5142, ASM-5143). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S8-E7001-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **service team and the consumers of rwb-deviation (the app slice, the two screens, the self-service dispute of rwb-comms, the wave 4 harness and the owners of rwb-case, rwb-decision, rwb-document and rwb-source-data)**, we want **one tagged contract baseline for the X1 deviation — its two writes, its `deviation` element and lists, its two events, its consumed rows, its error set and its fakes**, so that **the X1 flow can be built and tested in parallel on both sides of every boundary without waiting for the live services**.

This story owns the shapes and nothing else:

- the OpenAPI 3.1 document with `POST /cases/{caseId}/deviations` and `PATCH /deviations/{deviationId}` on the target base, their request and answer elements, their access right, their idempotency rule and their error statuses (DP-13);
- the `deviation` element with the fields of DF-CAS-036 to DF-CAS-045 and the three closed lists of TSD S8 T3.2;
- the `DeviationRaised` and `DeviationCleared` envelopes, their topic, their data and their listeners;
- the consumed rows: the evidence pack of rwb-document, the customer facts of rwb-source-data and the case events of rwb-case, each with its owner, its budget and a placeholder for the name no source publishes;
- the workflow boundary to rwb-case as the child's input, signals and stage outcome, and no invented REST case-move or timer operation;
- the decision-record element of DP-03 with its write-before-change rule and its failure behaviour;
- the error envelope and the message set of section 14, and the seven fakes of section 12.8.

It does not own: any business outcome, row, event instance or case move (RWB-S8-E7001-APP); the DEV rule rows and their versions (rwb-decision); the case of record, its assignment and its timers (rwb-case); the documents and the customer facts (rwb-document, rwb-source-data); the roles and reference data (rwb-access); and the implementations of the library, the edge route and the fakes' platforms, which are platform stories.

### 2. Business rationale

A contract baseline is what lets a wave start on Day 1. The X1 flow crosses five boundaries - the case, the decision record, the documents, the customer facts and the event - and the plan carries no C row for any of them, so without a tagged baseline the app slice would wait for live services and the wave would slip (GAP-3052; ASM-5137, ASM-5138). The baseline also settles four facts the sources leave open:

- the two events are given as EV-06 and EV-07 with no names, while TSD S8 T5.3 publishes `DeviationRaised` and `DeviationCleared` (ASM-5134);
- the topic `rwb.deviation.events.v1` follows the naming rule of the context pack, although DP-14 is not in the pattern set of this key (ASM-5136);
- the evidence pack is read from rwb-document because the FSD names the Document hub, although the connection matrix's S8 row names no P5 call (ASM-5137);
- SCR-08 shows a deviation queue, but the Ownership Map gives this service two write operations and no read, so the queue is not published here (ASM-5142).

The business effect is the one the legacy story promises - a complaint pauses the stage clock, has one handler and one recorded decision and returns the case to where it paused (REQ-DVH-011, REQ-S8-003) - and the contract adds nothing to it. No business value is fixed here: the deviation codes, the raised-by and outcome lists, the escalation and the complaint service level stay reference data and rule rows read at their version, so a business person can change them without a contract release.

### 3. Preconditions

- RWB-PLT-E1027-CON is published with its writer schema and stub, so the decision-record element is declared against the library rather than invented (DP-03).
- RWB-PLT-N001-CON is published, so the two screens and the self-service dispute are served on the composite route's terms and no screen contract is duplicated here (DP-19).
- The platform naming and error-library elements are in force: one base, one topic, one queue and one login per service, one error envelope with one message ID per condition, and one `Idempotency-Key` rule.
- TSD S8 T3.1, T3.2, T4, T5.3, T6.1 and T-A.1 are available as the source of the element, the lists, the state machine, the two events, the rights and the two operations.
- The Ownership Map rows of S8 are accepted: one table `deviation`, two REST operations, two events EV-06 and EV-07, no job and one workflow `DeviationWorkflow` (context pack).
- The operations of the rwb-document evidence-pack read, of the rwb-source-data customer-fact read and the names of the rwb-case events are Not specified in the source documents (GAP-3052; ASM-5137, ASM-5138, ASM-5139).
- No approval is needed to publish a Draft baseline; the tag is applied when the contract tests pass and the consumers sign off.

### 4. Flow

1. The baseline is drafted from TSD S8 T-A.1: the two write operations with their purposes, their request and answer elements and their error sets, moved onto `/api/recovery/deviation/v1` (DP-13).
2. The `DeviationRequest`, `DeviationOutcome` and `Deviation` elements are written from DF-CAS-036 to DF-CAS-045, with the required flags of T3.1 and the three lists of T3.2 as published enumerations.
3. The two event envelopes are written on `rwb.deviation.events.v1` with the CloudEvents wrapper, the retry and `.dlt` topics and the listeners of the connection matrix.
4. The three consumed rows are recorded with their owners, their fields, their budgets and their placeholders for the names no source publishes.
5. The rwb-case boundary is recorded as the child's input, its signals and its stage outcome, carrying the case reference, the paused state, the return point and the rule with its version, and no case or timer property (ASM-5139).
6. The decision-record element is recorded against the library schema, with the write-before-change rule and the MSG-P7-003 failure path.
7. The error set, the message texts, the Case record right of both operations and the `Idempotency-Key` rule are recorded; the queue read is explicitly not declared (ASM-5142).
8. Seven fakes are published, each answering the paths its consumers exercise, and the drift test compares each one with the document.
9. The baseline is reviewed by the app slice, the two screens, the self-service dispute, the wave 4 harness and the four consuming owners, tagged and handed over.
10. A later additive change is published inside major version 1; a removal, a rename or a retype opens a new major version.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A consumer asks for a property this document does not declare | The answer fails schema validation at the consumer, not at the service | MSG-GEN-001 | AC2 |
| X2 | A fake drifts from the document | The drift test fails and the baseline returns to review | None (pipeline log) | AC6 |
| X3 | A `v_ace_*` property, a `recovery_case` property or an ACE table read is added to the document | The absence test fails the build and the change is refused | None (pipeline log) | AC4, AC6 |
| X4 | A queue read, a second topic, a second event or a Schedule is declared | The absence test fails the build | None (pipeline log) | AC5, AC6 |
| X5 | A breaking change is proposed inside major version 1 | The review refuses it and a new major version is opened | None | AC1 |
| X6 | A property carries personal data | The schema test fails and the property is removed | None (pipeline log) | AC2, AC3 |

X1 to X6 are the failure paths of the artefact, not of a business transaction; the business failure paths are RWB-S8-E7001-APP's.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; it starts on Day 1 from TSD S8, the Ownership Map and the two platform baselines and needs no running service |
| Negotiable | The element names, the wording of the descriptions and the shape of the fakes are the author's choice; the operations, the fields, the lists, the events, the listeners and the budgets are fixed by the sources |
| Valuable | The app slice, the two screens, the self-service dispute and the wave 4 harness build on Day 1 against a tagged document and seven fakes |
| Estimable | One OpenAPI document, one AsyncAPI fragment, nine contract tables, one contract README and seven fake mapping sets |
| Small | Finished inside one week with the consumer sign-off |
| Testable | Each criterion is a validation of the document or a drift test of a fake, run in the pipeline |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the X1 deviation of rwb-deviation

  Background:
    Given the platform naming and error library is in force
    Given ownership is read from the Ownership Map and Architecture v5: deviation is S8, recovery_case queue assignment and timer are P3, decision_log_entry and rule_row are P7, document is P5, every v_ace_* view is P1

  Scenario: AC1 The two writes are declared on the deviation base with their shapes, rights and errors (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-deviation is produced with this change
    When it is validated against the OpenAPI 3.1 schema and the additive rule
    Then it validates with no error
    Then it declares POST /cases/{caseId}/deviations answering Deviation with status 200 or 201 and PATCH /deviations/{deviationId} answering Deviation with status 200, both under the base /api/recovery/deviation/v1 and owned by rwb-deviation
    Then both declare the Case record right U with the scope applied, the POST declares the Idempotency-Key header and the PATCH declares none
    Then the answers 400, 401, 403, 404, 409, 422 and 503 are declared with the one error envelope and one message ID per condition of section 14
    Then no read operation is declared on the base and the document names the deviation queue as served elsewhere (ASM-5142)

  Scenario: AC2 The deviation element, its required flags and its three closed lists are fixed (new, D-RCV-60)
    Given the deviation section of the document
    When it is compared with TSD S8 T3.1 and T3.2
    Then the Deviation element declares id, case_id, deviation_code, raised_at, raised_by, paused_state, handler_user_id, contact_stop, cleared_at and outcome, which are DF-CAS-036 to DF-CAS-045
    Then id, case_id, deviation_code, raised_at, raised_by, paused_state and contact_stop are required and the other three are optional
    Then deviation_code is published against LOV-DEVIATION with its seven values, raised_by against LOV-RAISED-BY with its four values and outcome against LOV-DEV-OUTCOME with its three values
    Then no property is added for a case route state, a timer, a document, a customer fact or a rule row, and those facts are named as other owners'
    Then no property carries personal data and no schema default carries a business value

  Scenario: AC3 The two events are declared with their envelopes, data and listeners (new, D-RCV-60)
    Given the event section of the document
    When it is compared with the Ownership Map rows of S8, TSD S8 T5.3 and the connection matrix
    Then DeviationRaised (EV-06) and DeviationCleared (EV-07) are declared on the topic rwb.deviation.events.v1 with the names rwb.deviation.DeviationRaised.v1 and rwb.deviation.DeviationCleared.v1, produced by rwb-deviation
    Then their listeners are rwb-case, rwb-comms and rwb-reporting and no other consumer
    Then DeviationRaised carries the case reference, the deviation reference, the code, the raised-at, the paused state, the contact-stop flag and the rule ID with its version
    Then DeviationCleared carries the case reference, the deviation reference, the outcome, the cleared-at and the rule ID with its version and no personal data
    Then the envelope is CloudEvents, the topic declares its retry and .dlt topics, and the schema test fails any property that is personal data
    Then the document declares no second topic and no Schedule

  Scenario: AC4 The case boundary and the decision-record element are fixed without inventing an operation (new, D-RCV-60)
    Given the workflow section and the decision section of the document
    When they are compared with Architecture v5 slides 8 and 13 and the decision-record library schema
    Then the case boundary is declared as the child's input, its signals and its stage outcome, carrying the case reference, the paused state, the return point, the rule ID with its version and the clock signal
    Then the document declares no REST operation consumed from rwb-case for a case move or a timer pause, and records that the routing is Temporal and not REST (ASM-5139)
    Then one decision record is declared per rule outcome with the case reference, the deviation reference, the rule ID, the package version, the inputs reference, the outcome and the decided-at time, written before the deviation row changes
    Then the element declares the failure behaviour MSG-P7-003 and one healthy and one stopped chain in its stub

  Scenario: AC5 The consumed rows are declared and the other owners' facts stay with their owners (new, D-RCV-60)
    Given the consumed rows of the document
    When they are compared with the rwb-document and rwb-source-data contracts and the connection matrix
    Then one row declares the evidence-pack read of rwb-document with its document fields, one hop and a 2 s budget
    Then one row declares the customer and contact fact read of rwb-source-data with its freshness stamp, one hop and a 2 s budget
    Then one row declares the case events of rwb-case as consumed and its event names are Not specified in the source documents (GAP-3052; ASM-5139)
    Then the document declares no v_ace_* path, no v_ace_* property, no document blob and no grant on another owner's schema, and the boundary test fails a build that adds one

  Scenario: AC6 The seven fakes and the naming baseline answer the document and hold the boundary (new, D-RCV-60)
    Given the fakes and the naming section of the document
    When each fake is compared with the operation or the element it serves, and each name with the platform naming rule
    Then seven fakes answer the rwb-case workflow, the rwb-document evidence pack, the rwb-source-data facts, the rwb-decision package, the decision-record chain, the outbox relay and the composite route
    Then the drift test compares every fake with the document and fails the build on any difference
    Then the schema is rwb_deviation, the login is rwb_deviation, the topic is rwb.deviation.events.v1, the queue is rwb-deviation and the Java package is th.co.scb.ace.workbench.recovery.deviation
    Then the document names recovery_case, queue, assignment, timer, decision_log_entry, rule_row, document and every v_ace_* view as other owners' and consumes them only through their contracts or the workflow boundary
```

These six criteria are new under D-RCV-60 and test the artefact only. They restate no business outcome of RWB-S8-E7001-APP and copy no legacy criterion: the legacy criterion this key owns stays with the app slice word for word.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | `deviation` is rwb-deviation's, and the document declares its fields, its lists and its required flags on the `Deviation` element only | Context pack ownership rows; TSD S8 T3.1 and T3.2 |
| BR2 | The decision record is declared as an element written before the deviation row changes, through the local library; a failed write changes nothing | DP-03; TSD S8 T2; legacy AC2 of RWB-E7-001 |
| BR3 | The case, its assignment, its queues and its timers stay with rwb-case: the document declares the workflow boundary and no `recovery_case` property, and invents no case-move or timer operation | Architecture v5 slides 8 and 13; ASM-5139 |
| BR4 | The documents stay with rwb-document and the customer facts with rwb-source-data: the document declares both reads as consumed and no `v_ace_*` or blob property | DP-05, DP-11; ASM-5137, ASM-5138 |
| BR5 | Two events and no more, one topic and no second: `DeviationRaised` and `DeviationCleared` on `rwb.deviation.events.v1`, listened to by rwb-case, rwb-comms and rwb-reporting | Context pack ownership rows; TSD S8 T5.3; connection matrix; ASM-5134, ASM-5135, ASM-5136 |
| BR6 | The POST declares `Idempotency-Key` and the PATCH declares none; no read operation is declared on this base | TSD S8 T-A.2; ASM-5142 |
| BR7 | The vocabulary is closed: the three lists are published as enumerations and read at their version, and no list value is a constant of the code | TSD S8 T3.2; FSD S8 BR-S8-010 |
| BR8 | The DEVIATION state machine of the document is the 9-state, 22-rule table of TSD S8 T4 held in `deviation.state`; no case route state is declared | TSD S8 T4 and T3.0 |
| BR9 | No personal data in a schema, an example or a fake: identifiers, codes, instants and a rule version only | Template and Rules v1 §R7.2 s17 |
| BR10 | A change is additive inside major version 1; a removal, a rename or a retype opens a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |

### 9. State transitions

The lifecycle of the document, not of a deviation:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two writes, the element, the lists, the two events, the consumed rows, the case boundary and the fakes are described | In review |
| In review | Consumer sign-off | The app slice, the two screens, the self-service dispute, the wave 4 harness and the owners of rwb-case, rwb-document, rwb-source-data and rwb-decision accept the document and the fakes | Baselined |
| Baselined | Additive change | A property or a status is added inside major version 1 | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a list value changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | A `v_ace_*` property, a `recovery_case` property, a queue read, a second topic or a Schedule | In review |

The deviation states the document describes are the app slice's to drive: DEV_FLAGGED, DEV_WITH_OWNER, DEV_REJECTED, DEV_RESOLVED, DEV_REROUTE and RESUMED, over the table of TSD S8 T4; this baseline fixes the vocabulary and moves no record.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-deviation | Owns the OpenAPI and AsyncAPI documents and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change and confirms the two event names and the three consumed placeholders (GAP-3052) |
| Consuming teams (the app slice, the two screens, the self-service dispute, the wave 4 harness and the owners of rwb-case, rwb-document, rwb-source-data and rwb-decision) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox library this document reuses |
| Data steward | Confirms that no personal data property is declared in an answer, an element or a fake |

### 11. Data

The baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Deviation element | `id`, `case_id`, `deviation_code`, `raised_at`, `raised_by`, `paused_state`, `handler_user_id`, `contact_stop`, `cleared_at`, `outcome` (DF-CAS-036 to DF-CAS-045) |
| Required flags | `id`, `case_id`, `deviation_code`, `raised_at`, `raised_by`, `paused_state` and `contact_stop`; `handler_user_id`, `cleared_at` and `outcome` optional |
| Lists | `LOV-DEVIATION` (X1 to X7), `LOV-RAISED-BY` (SCREENING_AGENT, RULE, OFFICER, CUSTOMER_CONTACT) and `LOV-DEV-OUTCOME` (RETURNED, RE_ROUTED, CASE_ENDED), published as enumerations |
| Event data | Case and deviation references, code, raised-at, paused state, contact-stop flag, outcome, cleared-at and the rule ID with its version |
| Decision record | The library element of DP-03, written before the deviation row changes |
| Consumed fields | The document fields of DF-DOC-001 to DF-DOC-011 and the customer facts behind the data-product read, read on their owners' contracts and never copied |
| Not declared here | `recovery_case`, `queue`, `assignment`, `timer`, `decision_log_entry`, `rule_row` and every `v_ace_*` view; the `state` column of TSD S8 T3.0 is declared as the record's lifecycle and moves no case |
| Consumed with no source | The operation names of the two reads, the names of the rwb-case events and the status-to-message mapping: Not specified in the source documents (GAP-3052; ASM-5137, ASM-5138, ASM-5139, ASM-5143) |

No table, no column and no migration is declared by this story; the schema and its Flyway sequence belong to the DB story of this service (DP-15).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-deviation (S8); base `/api/recovery/deviation/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/deviations` | `DeviationRequest` in, `Deviation` out (API-S8-001) | Case record, right U, scope applied | `Idempotency-Key` header |
| PATCH | `/deviations/{deviationId}` | `DeviationOutcome` in, `Deviation` out (API-S8-002) | Case record, right U, scope applied | Not applicable |

Both answer 400, 401, 403 with MSG-P4-002, 404, 409, 422 with MSG-GEN-001 and 503, each in the platform error envelope. The operation ids are those of TSD S8 T-A.1 and the paths are the target base, not the monolith form. The two operations are the whole of the service's REST surface in the Ownership Map; SCR-08's queue read is not published here (ASM-5142).

#### 12.2 REST operations consumed

| Operation | Owner | Use |
|---|---|---|
| The evidence-pack read; operation name Not specified in the source documents (GAP-3052; ASM-5137) | P5 rwb-document | The complaint documents of the case with their types, sources, storage references and index entries (DF-DOC-001 to DF-DOC-011); faked |
| The customer and contact fact read; operation name Not specified in the source documents (GAP-3052; ASM-5138) | P1 rwb-source-data | The facts a dispute is checked against, with the freshness stamp of the data product; faked |

Both are one hop with a 2 s budget, a GET retried once with jitter and a breaker per downstream (DP-11, ADR-020). Neither is a row of the plan's C list, which is empty (GAP-3052).

#### 12.3 Events published

| Event | Topic | Documented data | Listeners |
|---|---|---|---|
| `DeviationRaised` (EV-06, `rwb.deviation.DeviationRaised.v1`) | `rwb.deviation.events.v1`, with `.retry` and `.dlt` | Case reference, deviation reference, code, raised-at, paused state, contact-stop flag, rule ID and version; CloudEvents envelope; no personal data | rwb-case, rwb-comms and rwb-reporting (connection matrix column S8) |
| `DeviationCleared` (EV-07, `rwb.deviation.DeviationCleared.v1`) | `rwb.deviation.events.v1`, with `.retry` and `.dlt` | Case reference, deviation reference, outcome, cleared-at, rule ID and version; CloudEvents envelope; no personal data | rwb-case, rwb-comms and rwb-reporting (connection matrix column S8) |

The two ids are the events the Ownership Map gives S8; the two names are the events TSD S8 T5.3 publishes; the pairing of id to name is recorded as ASM-5134. The outbox that relays both is the platform library of DP-09, which the pattern set of this key does not carry (ASM-5135).

#### 12.4 Events consumed

| Event | Owner | Use |
|---|---|---|
| The case events of rwb-case; event names Not specified in the source documents (GAP-3052; ASM-5139) | P3 rwb-case | Keeps an open deviation aligned with the case it belongs to; a case that closes ends its open X1 with `CASE_ENDED` |

The S8 row of the connection matrix names an event subscription to P3 and no event name is published, so the consumer group is declared against the placeholder and faked. No other event is consumed and no inbox of this service is declared for any other topic.

#### 12.5 Workflows and activities

| Name | Type | Queue | Contract element |
|---|---|---|---|
| `DeviationWorkflow` | Workflow, one execution per case, started at any time, child of `CaseWorkflow`, parent close policy ABANDON, continues-as-new | `rwb-deviation` in namespace `rwb-recovery` | The child's input, its signals and its stage outcome; the case reference, the paused state, the return point and the rule with its version cross this boundary |
| `evaluateDeviationRules`, `recordAndApplyDeviation`, `resolveDeviation` | Activities, the three steps the app slice builds | `rwb-deviation` | The rule and package input, the decision and row output, and the outcome and event output of each step |

The case boundary is declared here and not as a REST row because the S8 row of the connection matrix names Temporal and events to P3, with no REST call (ASM-5139).

#### 12.6 Schedules

None. This baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table. The escalation of R-DEV-20 is a durable Temporal timer in the workflow and not a Schedule.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `deviation` | S8, `rwb_deviation` | The X1 record and the table both writes answer from |
| `decision_record` | Platform library in `rwb_deviation` | The local hash-linked record of the rule outcome (DP-03) |
| `idempotency_key` | Platform library in `rwb_deviation` | The raise key and the answer it holds |
| `outbox_event` | Platform library in `rwb_deviation` | The two event rows relayed to `rwb.deviation.events.v1` (DP-09 library) |

`recovery_case`, `queue`, `assignment`, `timer`, `decision_log_entry`, `rule_row`, `document` and every `v_ace_*` view are other owners' and are named only; no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case workflow fake | The case with its paused state and prescription date; an accepted `CLOCK_PAUSE`, `CLOCK_RESUME` and `ROUTE_D6`; a refused outcome; a case-closed event | AC4, AC5 |
| rwb-document evidence-pack fake | A complaint evidence pack; an empty pack; no answer inside 2 s; an unreadable answer | AC5 |
| rwb-source-data data-product fake | The customer facts of the case with a fresh stamp; a stale stamp | AC5 |
| rwb-decision package fake | The DEV package at its version with the rules of this service | AC4, AC6 |
| Local decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox; a stopped chain | AC4 |
| Outbox relay stub (`RWB-PLT-TE006-CON`) | A relayed `DeviationRaised` and `DeviationCleared`; a relay that fails and retries | AC3 |
| gateway-bff composite route fake | The merged SCR-06 and SCR-08 answer and the self-service raise of rwb-comms | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The four placeholder names are carried until their owners confirm them (GAP-3052).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 2 consumed | The two writes on `/api/recovery/deviation/v1`; the rwb-document and rwb-source-data reads; one hop, 2 s |
| Kafka | 2 published, 1 consumed | `DeviationRaised` and `DeviationCleared` on `rwb.deviation.events.v1`; the rwb-case case events; the decision record is the library's on `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 1 workflow and 3 activities declared | `DeviationWorkflow` on `rwb-deviation`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Deliverables.** The additive document `openapi/rwb-deviation-v1.yaml`, the `DeviationRequest`, `DeviationOutcome` and `Deviation` elements, the two envelopes in `asyncapi/rwb-deviation-v1.yaml`, the three lists as published enumerations, the contract README rows for the three consumed placeholders and the case boundary, the decision-record element against the library schema, and the seven WireMock mapping sets.

**Pattern application** (§R5.5)

| DP | Legacy marker | Pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H `RWB-PLT-E1027-CON` |
| DP-13 | `/api/recovery/v1` | `/api/recovery/deviation/v1` | None |
| DP-19 | Screen, ace-web | gateway-bff composite route | H `RWB-PLT-N001-CON` |

DP-13 moves the base of the two writes and nothing else. DP-19 puts SCR-06, SCR-08 and the self-service dispute behind the composite route. DP-09 and DP-14 are applied in fact and are not in the pattern set of this key (ASM-5135, ASM-5136).

**Build steps.** (1) Write the two writes and validate the additive rule. (2) Write the three elements, their required flags and the three lists. (3) Write the two envelopes with the no-personal-data, the listener and the no-second-topic tests. (4) Record the three consumed rows with their owners, budgets and placeholders. (5) Record the case boundary, the rights, the error envelope and the idempotency rule. (6) Record the decision-record element and validate it against the library schema. (7) Publish the seven fakes and the drift test. (8) Record the naming baseline and the absence tests, tag the baseline and collect the sign-off.

**Done when.** The document validates in the pipeline, the six contract tests pass, the seven fakes answer every declared path, the drift and absence tests are green, and the consumers have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required value of the raise or of the outcome is absent, invalid or fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Case record right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the deviation row changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The data product behind the case facts is stale after a late or failed batch (VR-S8-010-1); the check is the owner's | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-S8-001 | The raise succeeds and the saved state is shown; the message is the legacy one and carries the handler | {deviation} was raised. The case is with {handler}. |

The status-to-message mapping is not published by any source: 403 is the legacy refusal with MSG-P4-002, 422 the field error with MSG-GEN-001 and 503 the platform envelope, and the rest carry the platform's own conditions (GAP-3052; ASM-5143). The text of every message is the legacy and FSD S8 wording, copied unchanged.

### 15. Screens and states

| Screen | States served | What the baseline fixes |
|---|---|---|
| SCR-06 Raise deviation | Form; saved | The `DeviationRequest` element, the `Idempotency-Key` rule and the saved answer with MSG-S8-001 on `POST /cases/{caseId}/deviations` |
| SCR-08 Deviation queue | Loading; list | The `DeviationOutcome` entry and the `Deviation` answer on `PATCH /deviations/{deviationId}`; the queue list itself is not published here (ASM-5142) |

The composite route is RWB-PLT-N001-CON's and also calls rwb-case for the case, its owner and its timers; this baseline fixes the rwb-deviation answers only. The refusal, not-recorded and stale-data states read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-001-01 | AC1, AC2 | Contract | The raise and the outcome of a synthetic X1; the contract half answers the two writes and the `Deviation` element with its lists |
| TC-E7-001-02 | AC1, AC5 | Contract | The stopped decision-record stub and a stale product; the contract half answers the MSG-P7-003 path and the freshness rule |
| TC-E7-001-03 | AC1, AC5 | Contract | A role without the Case record right and a malformed request; the contract half answers the 403 with MSG-P4-002 and the 400 of the envelope |
| TC-E7-001-04 | AC1, AC5 | Contract | The rwb-document and rwb-source-data fakes with a full pack, an empty pack and no answer inside 2 s |
| TC-S8-E7001-CON-01 | AC1, AC2 | Contract | The document validates; the two writes, the base, the required flags, the three lists and the seven statuses are present |
| TC-S8-E7001-CON-02 | AC3 | Contract | The two envelopes validate against CloudEvents and the topic catalogue; the no-personal-data, the listener and the no-second-topic tests |
| TC-S8-E7001-CON-03 | AC4, AC5, AC6 | Contract | The case boundary and the decision element; the consumed rows and their placeholders; the seven fakes match the document, a drifted fake fails the build, and the no-`v_ace_*`, no-`recovery_case` and no-queue-read tests |

The four legacy ids are the legacy cases of RWB-E7-001 in their legacy order, carried as the contract half: each Covers value names the criterion that fixes the surface it exercises, and its business outcome is proved by RWB-S8-E7001-APP. The legacy level of these cases is not published per case, so each is mapped to `Contract` because the artefact under test is the contract (GAP-3052; ASM-5144). `TC-S8-E7001-CON-01` to `-03` are new. The full test text is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ids; the `-ITG` copies belong to the wave 4 harness.

### 17. Guardrails

- No business value in the contract: the deviation codes, the raised-by and outcome lists, the escalation and the complaint service level stay reference data or rule rows, never a schema default or a code constant.
- No personal data in a schema, an example or a fake: identifiers, codes, instants and a rule version only; every example is synthetic.
- The case stays with rwb-case and the documents with rwb-document: no `recovery_case` property, no timer property, no `v_ace_*` path, no blob property and no invented case-move operation (BR3, BR4).
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-deviation; a consumed operation is described as consumed and faked, never as provided (DP-01, DP-11).
- No retired element is reintroduced: the absence tests fail a build that declares a queue read, a consumed second event, a second topic, a Schedule, a Quartz row or a shared job table.

### 18. Traceability

| Legacy | Contract | Test |
|---|---|---|
| RWB-E7-001 AC2 | AC1, AC4 (the two writes and the decision element whose failure it asserts) | TC-E7-001-02, TC-S8-E7001-CON-01, TC-S8-E7001-CON-03 |
| RWB-E7-001 AC1 | AC1, AC2, AC5 (the shapes that carry the X1 record and its evidence) | TC-E7-001-01, TC-E7-001-04 |
| RWB-E7-001 TC-03 Access | AC1 (the right declared on both writes) | TC-E7-001-03 |
| RWB-E7-001 TC-04 Principle 5 | AC3, AC4 (the event and the decision element with their failure path) | TC-S8-E7001-CON-02, TC-S8-E7001-CON-03 |

| Source | What it supplies |
|---|---|
| TSD S8 T3.1, T3.2, T4, T5.3, T6.1 and T-A.1 | The `deviation` element and lists, the state machine, the two events, the rights and the two operations |
| FSD S8 A2.10, A1.1, Screens | The feature, its integration points, VR-S8-010-1, the roles and the two screens |
| Context pack S8 and the connection matrix | The schema, base, topic, queue, the two events, the one owned table and the listeners of P3, P6 and P9 |
| Architecture v5 slides 8, 11, 13 and 42 | The one-clock rule, the idempotency rule, the stage boundary and the additive rule |
| Split plan, slice RWB-S8-E7001-CON | The lane, the wave, the release and the empty dependency rows (GAP-3052) |

### 19. Out of scope

- Any business outcome: the row, the event instance, the decision record instance and the case move (RWB-S8-E7001-APP).
- The shapes of the other six codes, of the screening agent, of the two-deviation case, of the contact breach, of the override review and of the complaint-to-contact matching - each belongs to its own story of this service.
- The case of record, its route state, its assignment and its timers (rwb-case); the documents (rwb-document); the customer facts and the `v_ace_*` views (rwb-source-data); the DEV package and the ledger (rwb-decision); the roles and reference data (rwb-access); the notices and the self-service journey (rwb-comms).
- The schema, the login, the deployment, the observability and the pipeline (the DB, INF and OPS stories of this legacy key); the composite route and the platform libraries, which are RWB-PLT-N001-CON's and the platform's.
- Any change to a legacy file, to a master or to built Epic 1 and Epic 2 code.

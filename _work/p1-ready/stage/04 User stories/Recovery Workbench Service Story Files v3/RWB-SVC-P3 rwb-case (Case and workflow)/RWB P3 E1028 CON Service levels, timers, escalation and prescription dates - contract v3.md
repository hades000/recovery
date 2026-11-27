# RWB-P3-E1028-CON Service levels, timers, escalation and prescription dates

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- D-RCV-60 finishing pass: RD-P1-004.

| Item | Value |
|---|---|
| Story key | RWB-P3-E1028-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-028 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-P3-E1028-CON-14); confirm the sign-off with the epic design record |
| Size | Not specified in the source documents (DOR-RWB-P3-E1028-CON-16) |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract version | v1 (REST base `/api/recovery/case/v1`) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-012, FR-P3-014, FR-P3-015, FR-P3-016, FR-P3-022, FR-P3-025, FR-P3-030) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-004 |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-028 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (16 resolved, 25 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 27 November 2026: D-RCV-60 P1 developer readiness (RD-P1 register).

### 1. Story

As a **tech lead**, I want **the published contract baseline of the timer capability of rwb-case — `GET /api/recovery/case/v1/cases/{caseId}/timers` and the `prescriptionDate` of `GET /api/recovery/case/v1/cases/{caseId}`, the `Timer` and `Case` resources, the `rwb.case.TimerBreached.v1` event, the three consumed contracts, the retirement of the `TimerDue` event, the nine contract tables and the four fakes**, so that **the app, operations and test stories of this legacy key build against one fixed, testable contract on Day 1 and a timer field, an escalation field or an event can never drift between rwb-case, rwb-source-data and the ledger without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The capability exposes a deadline that a team manager, a court file and an auditor all rely on, and it is written by a workflow that no consumer can see: the only thing a consumer can trust is the shape of the answer. Two failure modes are therefore worth a contract of their own. A renamed escalation field would make a breach invisible on the screen while the workflow still raised it. A `TimerDue` event that reappeared on a topic would put a second, contradictory clock in the estate after the job behind it was retired.

The baseline also fixes the naming the checks rely on: schema `rwb_case`, REST base `/api/recovery/case/v1`, topic `rwb.case.events.v1`, event names `rwb.case.<Event>.v1`, task queue `rwb-case` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.case` (DP-13, DP-14). It records the two elements the target retires — `JOB-05` Timer check and the `TimerDue` event (EV-18) — and keeps `TimerBreached` as event #19 of `rwb.case.events.v1` (Architecture v5 slides 42 and 44).

The boundary with the sibling contract story is explicit: **this baseline fixes what the timer story writes** — `warnAt`, `expiresAt`, `status`, `escalationLevel`, `escalatedToRole`, `escalatedAt` and `prescriptionDate`; **RWB-P3-E2015-CON adds** `nextStepOwnerRole`, `nextEscalationRole` and `inWarning` for the case record view. Neither document restates the other's field.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the document, topic and event names follow the platform rule.
- The platform error envelope, the CloudEvents 1.0 envelope, the retry and `.dlt` topic convention and the Idempotency-Key rule are the platform baseline (RWB-PLT-EVT, RWB-PLT-TE006-CON).
- The operations and their owners are taken from the Ownership Map only; this document never declares another service's operation as provided.
- RWB-P3-E1028-APP is the writer this baseline serves; the timer boundary inside `CaseWorkflow` is its implementation, so this story fixes the shape and never the mechanism.
- RWB-P3-E2015-CON extends the same `Timer` resource, so this document leaves room for its three added fields.
- The escalation columns DF-WRK-043 and DF-WRK-044 are absent from the TSD and the logical model; their field-level detail is Not specified in the source documents (GAP-2203; ASM-3618).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document: the `Timer` resource, the `Timer[]` answer of `GET /cases/{caseId}/timers`, the `prescriptionDate` of `GET /cases/{caseId}`, and the error envelope of both.
2. Fix the ordering rule of the `Timer[]` answer and the meaning of every date field, so no consumer sorts or recomputes on its own.
3. Draft the AsyncAPI 3 fragment of `rwb.case.events.v1` for `rwb.case.TimerBreached.v1`, and state the retirement of `TimerDue` as an absence in the same document.
4. Record the three consumed operations with their owner, their use, the 2 s budget and the error mapping.
5. Record the decision-record element on `rwb.decision-record.v1` as consumed from the library (DP-03) and not as a provided event.
6. Publish the nine contract tables of section 12 and the four fakes.
7. Add the contract tests: schema validation, ordering, the additive rule, the error mapping, the drift between a fake and the document, and the absence of the retired elements.
8. Tag the baseline and hand it to RWB-P3-E1028-APP, RWB-P3-E1028-OPS, RWB-P3-E2015-CON and the wave 1 harness RWB-ITG-E1028-ITG.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the error envelope | MSG-P3-030 | AC1 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1 |
| X3 | A consumer cannot deserialise `TimerBreached` | The registry compatibility run fails the build; the event is not published | None | AC2 |
| X4 | A retired element reappears in the document or a topic | The absence test fails: no `TimerDue` event and no timer-check job | None | AC2 |
| X5 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC5 |
| X6 | A consumed path has no Ownership Map row, or its field-level detail is missing | The row carries the gap and the assumption; the fake is derived from the owner's published document | None | AC3 |
| X7 | The two sibling documents disagree on an escalation field | The review fails and the field is fixed in one document only | None | AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reuses the platform envelopes, the Ownership Map and the published documents of the consumed services |
| Negotiable | Field-level lengths and examples are settled in the baseline review; the operations, the event and the retired elements are fixed by the target |
| Valuable | Unblocks the app, operations and test stories of this legacy key and fixes the meaning of a deadline for every consumer |
| Estimable | Two artefacts, one event element, three consumed rows, nine contract tables, four fakes and six contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, never against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the service levels, timers, escalation and prescription dates

  Background:
    Given the service naming rule of the platform library is in force
    Given the rwb-case base is /api/recovery/case/v1 and the topic is rwb.case.events.v1
    Given the timer story RWB-P3-E1028-APP is the writer this baseline serves

  Scenario: AC1 The OpenAPI document declares the two read operations and the Timer resource (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-case is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares GET /cases/{caseId}/timers with the Timer array and GET /cases/{caseId} carrying prescriptionDate, both under the base /api/recovery/case/v1 and owned by rwb-case
    Then the Timer resource carries id, caseId, timerType, startedAt, expiresAt, warnAt, paused, status, escalationLevel, escalatedToRole and escalatedAt
    Then timerType is a closed LOV-TIMER code (nine values), status is a closed LOV-TIMER-STATUS code (four values) and escalatedToRole is a role code and not a display name
    Then escalatedToRole and escalatedAt are optional and are declared as written by the timer story
    Then both operations name their security right, their 2 s budget and their error responses 401, 403, 404 and 503
    Then every property is additive within major version 1, so the reader of RWB-P3-E2015-CON can extend the same resource

  Scenario: AC2 The TimerBreached event is declared and the retired elements are absent (new, D-RCV-60)
    Given the AsyncAPI 3 fragment of rwb.case.events.v1
    When it is reviewed against the event catalogue
    Then rwb.case.TimerBreached.v1 is declared as event 19 with the key caseId and the payload caseId, caseNo, timerId, timerType, expiresAt and escalateTo
    Then the payload carries no name, address, identity number, contact point or amount
    Then the registry compatibility run passes against the previous version of the event
    Then the document declares no TimerDue event and no timer-check job, and the absence test fails a document or a chart that declares one
    Then TimerDue is recorded as retired as "timer inside the workflow" with the slide that retires it

  Scenario: AC3 The consumed contracts carry their owner, the 2 s budget and one gap row (new, D-RCV-60)
    Given the consumed operations of the document
    When they are compared with the Ownership Map
    Then GET /api/recovery/source-data/v1/accounts/{accountId} names P1 rwb-source-data as its owner
    Then GET /api/recovery/source-data/v1/calendar/holidays names P1 rwb-source-data as its owner, and its exact path carries the placeholder Not specified in the source documents (GAP-2202; ASM-3616)
    Then POST /api/recovery/access/v1/authorise names P4 rwb-access as its owner
    Then every consumed row states one hop, the 2 s timeout, the GET retry once with jitter and the breaker per downstream
    Then the decision-record element on rwb.decision-record.v1 is declared as consumed from the library of P7 and not as a provided event
    Then every failure of a consumed call maps to 401, 403, 404, 503 or the retry path, never to an empty timer list that reads as "no timer"

  Scenario: AC4 The error envelope and the message IDs are fixed for every failure (new, D-RCV-60)
    Given the four error responses of each operation
    When they are reviewed against the message register
    Then 401 carries MSG-P4-001, 403 carries MSG-P4-002 with the Case record right, 404 carries MSG-P4-003 and 503 carries the platform unavailable text
    Then a schema failure of a request or a response maps to MSG-P3-030 with the error envelope and no stack trace
    Then the business texts of MSG-P3-003, MSG-P3-004, MSG-P3-026 and MSG-P7-003 are copied unchanged from the legacy story
    Then no error answer carries a customer field or an internal identifier of another service

  Scenario: AC5 The four contract fakes match the document and drift fails the build (new, D-RCV-60)
    Given the four fakes of section 12.8
    When the drift test compares each fake with the document
    Then the rwb-source-data fake answers the account dates and the calendar, including an account with no last payment date and a delayed answer beyond 2 s
    Then the rwb-access fake answers a granted read, a refused role and a refused scope
    Then the decision-record double answers a sealed record with R-UNI-30 and an unavailable answer
    Then the deviation fixture carries DeviationRaised on 2026-12-02 and DeviationCleared on 2026-12-04
    Then a changed field, a changed status code or a changed payload in any fake fails the build

  Scenario: AC6 The nine contract tables are complete and the boundary with the sibling document holds (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then 12.6 records None and names JOB-05 as retired
    Then the fields nextStepOwnerRole, nextEscalationRole and inWarning are absent here and belong to RWB-P3-E2015-CON
    Then the escalation columns escalatedToRole and escalatedAt carry their placeholder until the field-level detail is settled (GAP-2203; ASM-3618)

  Scenario: AC7 The ten business rules are proved by the guardrail and boundary checks (new, D-RCV-60)
    Given the ten business rules BR1 to BR10 of section 8 and the guardrails of section 17
    When the guardrail and boundary checks run against the two artefacts and the four fakes
    Then BR1 and BR7 hold: only the base /api/recovery/case/v1 and only operations owned by rwb-case are declared as provided
    Then BR2 and BR3 hold: every event name is rwb.case.<Event>.v1 on rwb.case.events.v1, keyed by caseId, with the CloudEvents 1.0 envelope and no personal data
    Then BR4 holds: no read declares an Idempotency-Key
    Then BR5 holds: one error envelope and one message ID per condition, with the business texts copied unchanged from the legacy story
    Then BR6 holds: every schema change is additive within major version 1 and a breaking change is a new major version
    Then BR8 holds: the durable timer inside CaseWorkflow is authoritative and the contract fixes what the workflow writes, never the mechanism
    Then BR9 holds: no TimerDue event, no timer-check job and no Schedule is declared
    Then BR10 holds: no level, warning percentage, escalation role, legal period, warning day or timeout is fixed in the contract
```

These six criteria are new for the contract baseline and test the artefact only; they restate no business outcome owned by RWB-P3-E1028-APP. The wave 1 harness RWB-ITG-E1028-ITG consumes this baseline and copies none of these criteria.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/case/v1`; the document never declares another service's path as provided | DP-13; Template and Rules §R4 |
| BR2 | Event names are `rwb.<short>.<Event>.v1` on `rwb.<short>.events.v1`, with retry and `.dlt` topics | DP-14; Template and Rules §R4 |
| BR3 | Every event carries the CloudEvents 1.0 envelope, is keyed by `caseId` and carries no personal data | Architecture v5 slides 42 and 43; DP-09 |
| BR4 | A read declares no Idempotency-Key; only a POST declares one and stores its answer | Architecture v5 slide 11; DP-09 |
| BR5 | One error envelope and one message ID per condition; the business texts are copied unchanged from the legacy story | Template and Rules §R7.2 s14 |
| BR6 | A schema change is additive within a major version; a breaking change is a new major version | Architecture v5 slide 42 (BACKWARD compatibility) |
| BR7 | The document lists only operations owned by rwb-case; a consumed operation is described as consumed, never as provided | Ownership Map v1 |
| BR8 | The timer is a projection and the clock is a durable Temporal timer inside `CaseWorkflow`; the durable timer is authoritative and the timer row is its audit copy, written by ApplyStateActivity in the same transaction as the state and read back on a reopen; the contract fixes what the workflow writes and never the mechanism | ASM-0078; DP-10 |
| BR9 | No `TimerDue` event and no timer-check job or Schedule is declared: both are retired | Architecture v5 slides 42 and 44 |
| BR10 | No business value is fixed in the contract: levels, warning percentage, escalation roles, legal periods, warning days and timeouts stay data or service configuration | Template and Rules §R7.2 s17 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the `Timer` resource and the event are described | In review |
| In review | Consumer sign-off | The app, operations and test stories and the P1, P4 and P7 owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1, for example the three fields of RWB-P3-E2015-CON | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped | New major version drafted |
| Baselined | Drift in a fake | The drift test of AC5 fails | In review |
| Baselined | Retired element reappears | The absence test of AC2 fails | In review |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-case | Owns the OpenAPI and AsyncAPI documents and the fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the field-level detail of the escalation columns |
| Consuming teams (app, operations, test, the P1, P4 and P7 owners, and RWB-P3-E2015-CON) | Review and sign off the parts they consume |
| Platform library owner | Owns the CloudEvents envelope, the error envelope and the naming rule this document reuses |
| Data steward | Confirms that no personal data field is declared in an event or an answer |

The per-service login behind the security scheme is not part of this baseline; the document names the scheme "the rwb-case login (DP-02)".

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Timer resource | `id`, `caseId`, `timerType`, `startedAt`, `expiresAt`, `warnAt`, `paused`, `status`, `escalationLevel`, `escalatedToRole`, `escalatedAt`, from `timer` DF-WRK-027 to DF-WRK-036 and DF-WRK-043 to DF-WRK-044 | Not specified in the source documents (DOR-RWB-P3-E1028-CON-7) |
| Case resource | `caseNo`, `productGroup`, `status`, `queueId`, `ownerUserId`, `prescriptionDate`, `deviationOpen`, `legalHold`, from `recovery_case` DF-CAS-001 to DF-CAS-020 | Not specified in the source documents (DOR-RWB-P3-E1028-CON-7) |
| Event payload | `caseId`, `caseNo`, `timerId`, `timerType`, `expiresAt`, `escalateTo`; IDs, codes and dates only | Not specified in the source documents (DOR-RWB-P3-E1028-CON-7) |
| Consumed answers | Account dates DF-ACE-007 and DF-ACE-026 and the calendar DF-ACE-155 and DF-ACE-159 through P1; the right and the scope through P4; the sealed record through P7 | Not specified in the source documents (DOR-RWB-P3-E1028-CON-7) |

The field-level types, lengths and required flags of `escalatedToRole` and `escalatedAt` are Not specified in the source documents (GAP-2203; ASM-3618); this story fixes their names, their optionality and their meaning.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-case (P3); base `/api/recovery/case/v1`.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| GET | `/cases/{caseId}/timers` | `Timer[]` ordered by `expiresAt` ascending, a timer without `expiresAt` last; the fields of section 11 | Case record R, scope applied |
| GET | `/cases/{caseId}` | Case with `prescriptionDate` beside `caseNo`, `productGroup`, `status`, `queueId`, `ownerUserId`, `deviationOpen` and `legalHold` | Case record R, scope applied |

Both answer 401, 403, 404 and 503 with the error envelope; neither takes an Idempotency-Key. The `Case` resource itself is owned by RWB-P3-E1018-CON and this baseline declares only `prescriptionDate` on it. The three fields `nextStepOwnerRole`, `nextEscalationRole` and `inWarning` are added to the same `Timer` resource by RWB-P3-E2015-CON and are not declared here.

The `timerType` and `status` properties are closed lists — LOV-TIMER with nine values and LOV-TIMER-STATUS with four — read through the reference-data contract of rwb-case (DP-07). The document fixes the enum of each list, so a value outside it fails schema validation and a new list value is a change to this baseline.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| GET | `/api/recovery/source-data/v1/accounts/{accountId}` | P1 rwb-source-data | Contract date, last payment date and data as of, faked; the exact answer shape is taken from the P1 document (GAP-2202; ASM-3616) |
| GET | `/api/recovery/source-data/v1/calendar/holidays?from={from}&to={to}` | P1 rwb-source-data | The non-working days for the working-day count, faked; the path is the placeholder of AC3 (GAP-2202; ASM-3616) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The Case record R and scope check on both reads, faked |

Every row is one hop with a 2 s timeout, a GET retry once with jitter and a breaker per downstream. The decision-record element is consumed from the library of P7 on `rwb.decision-record.v1` (DP-03) and is not a REST row.

#### 12.3 Events published

| Event | Topic | Owner | Schema element |
|---|---|---|---|
| `rwb.case.TimerBreached.v1` (event 19) | `rwb.case.events.v1` | P3 rwb-case | caseId, caseNo, timerId, timerType, expiresAt, escalateTo; published by the durable timer in RWB-P3-E1028-APP |
| `rwb.decision.DecisionRecorded.v1` (event 08) | `rwb.decision-record.v1` | P7 rwb-decision | The record reference, ruleId, ruleVersion, decidedAt, escalateTo; published by the local library (DP-03) |

This story declares the two elements because the capability depends on them; it publishes neither itself. `TimerDue` (EV-18) is retired and is declared nowhere as published.

#### 12.4 Events consumed

| Event | Topic | Owner | Consumer contract element |
|---|---|---|---|
| `rwb.case.CaseCreated.v1` | `rwb.case.events.v1` | P3 rwb-case | caseId, caseNo, createdOn; starts the prescription calculation |
| `rwb.case.CaseAllocated.v1` | `rwb.case.events.v1` | P3 rwb-case | caseId, queueId, ownerId; starts the `SERVICE_LEVEL` timer |
| `rwb.case.CaseTransferred.v1` | `rwb.case.events.v1` | P3 rwb-case | caseId, fromQueueId, toQueueId, reason; stops and restarts the timer |
| `rwb.case.CaseStateChanged.v1` | `rwb.case.events.v1` | P3 rwb-case | caseId, fromStatus, toStatus; stops and restarts the timer |
| `rwb.deviation.DeviationRaised.v1` (event 06) | `rwb.deviation.events.v1` | S8 rwb-deviation | caseId, deviationCode, raisedAt; pauses the stage timer (wave 2) |
| `rwb.deviation.DeviationCleared.v1` (event 07) | `rwb.deviation.events.v1` | S8 rwb-deviation | caseId, deviationCode, clearedAt, outcome; resumes the timer (wave 2) |

Every row is keyed by `caseId`, carries the CloudEvents envelope and has the inbox dedupe with the retry and `.dlt` path.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| CaseWorkflow | Workflow, parent, one per case, workflow ID = `case-{caseId}` | `rwb-case` | Holds the durable `SERVICE_LEVEL` and `PRESCRIPTION` timers and raises `TimerBreached`; the writer this baseline serves |
| EvaluateRules | Activity | `rwb-case` | The level, the warning point and the escalation role from the parameter and reference rows, with the rule ID and version |
| RecordAndApply | Activity | `rwb-case` | The record, the projection and the outbox in one transaction |

No Schedule and no Quartz job is declared by this baseline.

#### 12.6 Schedules

None. `JOB-05` Timer check and its five-minute Quartz schedule are retired with the `TimerDue` event (Architecture v5 slides 42 and 44; ASM-0078), and this baseline registers no Schedule, no cron entry and no job name. `JOB-02`, `JOB-03` and `JOB-06` belong to other stories of this service and are not declared here.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| timer | P3 (rwb_case) | The projection the timers operation reads and the timer story writes |
| recovery_case | P3 (rwb_case) | `prescription_date` and the case facts of the second operation |
| queue | P3 (rwb_case) | The team code the escalation role is resolved against |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_case | The envelope of the two event rows and the inbox dedupe |

`v_ace_account` and `v_ace_holiday` are ACE views read only through rwb-source-data; no cross-schema read and no foreign key into another schema (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data WireMock | The account dates of RW-2026-000402 and RW-2026-000405, an account with no dates, the calendar with 2026-12-05 to 2026-12-07 non-working, and a delayed answer beyond 2 s | App story, operations smoke profile, contract tests |
| rwb-access WireMock | `POST /authorise` with a granted answer, a refused role and a refused scope | App story, operations smoke profile, contract tests |
| rwb-decision record double | A sealed record of a warning and of a breach with `R-UNI-30`, and an unavailable answer | App story, contract tests |
| rwb-deviation event fixture | `DeviationRaised` on 2026-12-02 and `DeviationCleared` on 2026-12-04 for RW-2026-000408 | App story, contract tests |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed | Timers and case provided; account dates, calendar and authorise consumed; one hop, 2 s |
| Kafka | 2 declared as published by their owners, 6 declared as consumed | TimerBreached and DecisionRecorded; four case events and two deviation events |
| Temporal | 1 workflow, 2 activities, no Schedule | CaseWorkflow with the durable timers; EvaluateRules and RecordAndApply |
| File | None | No file in this contract |

### 13. Solution plan

**Deliverables.** The change to `openapi/rwb-case-v1.yaml` with the `Timer` resource and the timers operation, the AsyncAPI 3 fragment of `rwb.case.events.v1` that names `TimerBreached` and records `TimerDue` as retired, the contract README rows for the ordering, the retirement and the boundary with RWB-P3-E2015-CON, and the four fake assets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/case/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.case.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The rows record what the baseline has to describe; no dependency is a build dependency of this story, which is Day 1 by rule.

**Build steps**

1. Add the `Timer` resource and the `Timer[]` answer, with the ordering rule and the optionality of the two escalation fields; validate the additive rule of AC1 in the pipeline.
2. Add `prescriptionDate` to the `Case` resource and leave the three fields of RWB-P3-E2015-CON out of this document.
3. Write the AsyncAPI fragment for `TimerBreached` with its key and payload, and record `TimerDue` as retired with its slide.
4. Add the absence test that fails a document or a chart declaring a `TimerDue` event, a timer-check job or a timer-check Schedule.
5. Record the three consumed rows with their owner, their budget and the placeholder of the calendar path; map every failure code to the envelope and a message ID.
6. Publish the four fakes and the six contract tests; a drift between a fake and the document fails the build.
7. Baseline tag and the consumer sign-off note, including the P1, P4 and P7 owners, RWB-P3-E2015-CON and the wave 1 harness.

**Done when.** The OpenAPI and AsyncAPI artefacts validate in the pipeline, the six contract tests pass, the four fakes answer every consumed path and the drift test is green, and the app, operations and test stories have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-003 | A timer or the prescription date is inside its warning period | {timer} ends on {date}. |
| MSG-P3-004 | The case is on hold for a deviation | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-P3-026 | No service level or legal period found | No {item} is set for {scope}. The timer did not start. |
| MSG-P3-030 | A request or a response fails schema validation | The request could not be read: {detail}. |
| MSG-P7-003 | The decision record could not be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-001 | No session on a read | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-002 | Role without Case record R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case unknown or outside the scope | This case is not in your scope. |

The four business texts are copied unchanged from the legacy story; MSG-P3-030, MSG-P4-001 and MSG-P4-003 are the platform envelope texts. Thai text follows DL10 (open; assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863).

### 15. Screens and states

The contract serves SCR-03 Case record in its Read only, On hold and Loading states and SCR-09 Exception queue in its Loading and List states, through the gateway-bff composite route (DP-19). The empty, error and no access states of SCR-03 are Not specified in the source documents (CG-ALL-3639), and those of SCR-09 are Not specified in the source documents (CG-ALL-3640). It fixes the two rwb-case answers only: the case field list, the timer panel, the escalation state and the exception list belong to RWB-P3-E2015-APP and RWB-P3-E1035-CON.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P3-E1028-CON-01 | AC1 | Contract | The document validates; the two operations and the eleven `Timer` properties; a timer with no `expiresAt` sorts last |
| TC-P3-E1028-CON-02 | AC2 | Contract | The `TimerBreached` message; the registry compatibility run; the absence test for `TimerDue`, the timer-check job and the Schedule |
| TC-P3-E1028-CON-03 | AC3 | Contract | Three consumed rows with their owner, the 2 s budget, the retry rule and the calendar placeholder |
| TC-P3-E1028-CON-04 | AC4 | Component | The four error responses with their message IDs; a schema failure with MSG-P3-030; no stack trace |
| TC-P3-E1028-CON-05 | AC5 | Component | Four fakes compared with the document; a changed field, status or payload fails the build |
| TC-P3-E1028-CON-06 | AC6 | Component | The nine sub-tables with owners; 12.6 None with no timer-check job declared; the three fields of the sibling document absent here |
| TC-P3-E1028-CON-07 | AC6; BR1; BR7 | Component | Boundary: each row of the §12.7 tables has a named owner; a row with no owner fails the build |
| TC-P3-E1028-CON-08 | BR2 to BR6; BR8 to BR10 | Contract | Event names and envelope; no Idempotency-Key on a read; one error envelope; additive schema change; workflow timer; no TimerDue, timer-check job or Schedule; no business value fixed |
| TC-P3-E1028-CON-09 | AC7; BR1 to BR10 | Contract | Guardrail and boundary checks: one base and one topic per service, owned operations only, closed list values, one error envelope per condition, additive schema change, durable workflow timer, no retired element, no business value fixed |

The fourteen legacy test cases of RWB-E1-028 are owned by RWB-P3-E1028-APP and copied with the `-ITG` suffix by RWB-ITG-E1028-ITG; a contract story owns no business outcome and therefore no legacy test case. The P1 account-date and holiday inputs are proved in RWB-P3-E1028-APP, not here; this story asserts no TimerDue.

### 17. Guardrails

- No business value in the contract: levels, warning percentage, escalation roles, legal periods, warning days and timeouts stay data, reference data or service configuration.
- No personal data in a schema, an example or a fake: IDs, codes and dates only; no name, address, identity number, contact point or amount.
- The contract names only rwb-case tables and only operations owned by rwb-case; the P1 and P4 operations are consumed and faked, never declared as provided (DP-01).
- One REST base and one topic per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- ACE data is reached only through the owner's contract: no ACE view and no cross-schema join is declared.
- No retired element is reintroduced: the absence test of AC2 fails a document or a chart that declares a `TimerDue` event or a timer-check job.
- Every example is synthetic; no production payload is copied into a schema, an example or a fake.
- The error envelope, the CloudEvents envelope and the naming rule come from the platform library; this story narrows them and never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-CWC-011 | Service levels, warnings and escalation as data; a breach does not move the case | The `Timer` resource, its escalation fields, the `TimerBreached` payload and MSG-P3-003 | TC-P3-E1028-CON-01, TC-P3-E1028-CON-02 |
| REQ-CWC-012 | Prescription date from the legal periods at creation | `prescriptionDate` on the `Case` resource and the account-date and calendar rows consumed | TC-P3-E1028-CON-01, TC-P3-E1028-CON-03 |
| REQ-CWC-016 | Every timer event logged with rule and version | The decision-record element and its rule ID and version | TC-P3-E1028-CON-02, TC-P3-E1028-CON-03 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three consumed rows with their budget, retry and breaker | TC-P3-E1028-CON-03 |
| ADR-016 | Durable timers replace Quartz | The workflow rows and the absence of a timer-check job | TC-P3-E1028-CON-02 |

### 19. Out of scope

- The implementation of the timers, the prescription calculation and the two reads (RWB-P3-E1028-APP).
- The deployment, the consumer groups, the dashboards, the alerts and the runbook (RWB-P3-E1028-OPS).
- The three fields the case record view adds to the same resource (RWB-P3-E2015-CON) and the case record view itself (RWB-P3-E1035-CON, RWB-P3-E2015-APP).
- The Case record R right and its refusal (RWB-P4-E1028-APP) and the central ledger (RWB-P7-E1028-APP).
- The P1, P4 and S8 contracts themselves: consumed and faked, never defined here.
- The gateway-bff composite route and the screen field list (RWB-PLT-N001-CON).
- The cross-service journey harness and its evidence (RWB-ITG-E1028-ITG).

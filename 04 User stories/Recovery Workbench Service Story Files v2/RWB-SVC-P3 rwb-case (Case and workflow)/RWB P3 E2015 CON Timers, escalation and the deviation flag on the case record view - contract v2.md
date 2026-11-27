# RWB-P3-E2015-CON Timers, escalation and the deviation flag on the case record view

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E2015-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-015 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P3-E2015-CON-16) |
| Patterns applied | DP01, DP03, DP07, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract version | v1 (REST base /api/recovery/case/v1) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-014, FR-P3-015, FR-P3-016, FR-P3-019, FR-P3-020, FR-P3-021, FR-P3-022) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-015 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (15 resolved, 22 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the two read operations that put the clocks and the deviation flag on the case record view — `GET /api/recovery/case/v1/cases/{caseId}` with its `deviations[]` and `deviationsAvailable`, and `GET /api/recovery/case/v1/cases/{caseId}/timers` with its owner-role, escalation and warning fields — together with the consumed S8, P7 and P4 contracts, the event and workflow elements the capability depends on, the nine contract tables and three contract fakes**, so that **the app, operations and test stories of this legacy key build against a fixed, testable contract on Day 1 and a deviation answer, an approver answer or a timer field can never drift between rwb-case, rwb-deviation and rwb-decision without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The capability of RWB-E2-015 shows three sources on one screen: rwb-case for the case and its timers, rwb-deviation for the deviations, rwb-decision for the approver of each deviation, and rwb-access for the authorisation check. Two of those answers are composed inside rwb-case, so their field names, their empty and degraded shapes and their timeouts are the parts most likely to drift silently: an approver field renamed in the S8 or P7 contract would empty a panel at run time, and a `deviations[]` that disappears when the deviation service is slow would hide the on-hold banner instead of degrading one section.

The baseline also fixes the naming the checks require: schema `rwb_case`, REST base `/api/recovery/case/v1`, topic `rwb.case.events.v1`, event names `rwb.case.<Event>.v1`, task queue `rwb-case` in namespace `rwb-recovery` and Java package Not specified in the source documents (CG-ALL-4222). It records that TimerBreached is event #19 of the catalogue and stays on `rwb.case.events.v1` while JOB-05 Timer check and the TimerDue event are retired (Architecture v5 slides 42 and 44), so no contract in this story declares a timer-check job, a timer-check topic or a timer-check Schedule.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the document, topic and event names follow the platform rule rather than a local choice.
- The platform error envelope, the CloudEvents 1.0 envelope and the retry and `.dlt` topic convention are the platform baseline (RWB-PLT-EVT, RWB-PLT-TE006-CON); where this document narrows them it does so explicitly.
- The case record view contract RWB-P3-E1035-CON is published, so the Case resource this story extends has one owner document and the added fields are an additive change to it.
- The timer contract RWB-P3-E1028-CON is published, so the meaning of `warn_at`, `expires_at`, `inWarning`, `escalated_to_role`, `escalated_at` and `nextEscalationRole` is fixed by the story that writes them and not by this one.
- The operations and their owners are taken from the Ownership Map only; this document never declares another service's operation as provided.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the additive change to the rwb-case OpenAPI 3.1 document: the deviation object, `deviations[]` and `deviationsAvailable` on the Case resource, and the five added fields on the Timer resource.
2. Fix the ordering rule of the timers answer and the ordering rule of `deviations[]`, so two consumers never sort differently.
3. State the degraded shapes: the case answer with `deviationsAvailable` false and the empty list, the timers answer unchanged, and the timer answer never degraded by a deviation failure.
4. Record the three consumed operations with their owner, their use and the 2 s budget, and map every failure to the error envelope and a message ID.
5. Record the event elements: TimerBreached as event #19 of `rwb.case.events.v1` published by the timer story, DecisionRecorded on `rwb.decision-record.v1`, and the three events the timer story consumes.
6. Record the workflow element: the durable timer inside CaseWorkflow and the projection it writes, with no timer-check Schedule anywhere.
7. Publish the nine contract tables of section 12 and the three contract fakes.
8. Add the contract tests: schema validation, ordering, the degraded shape, the 2 s budget, the error mapping, the drift between a fake and the document, and the absence of a retired element.
9. Tag the baseline and hand it to RWB-P3-E2015-APP, RWB-P3-E2015-OPS and the wave 2 harness RWB-ITG-E2015-ITG.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the error envelope | MSG-P3-030 | AC1 |
| X2 | A consumer cannot deserialise a TimerBreached event | The registry validation fails the build; the event is not published | None | AC5 |
| X3 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1 |
| X4 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X5 | The consumed S8 read path is not in the Ownership Map | The row carries the gap and the assumption, and the fake is derived from the S8 published document | None | AC4 |
| X6 | A retired element reappears in the document, a job or a topic | The absence test fails: no timer-check Schedule, no TimerDue event, no timer-check topic | None | AC5 |
| X7 | A field-level definition is missing from the source material | The field is marked with the placeholder and one gap row is carried | None | AC2 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the two same-service contracts it extends and the Ownership Map only |
| Negotiable | Field-level detail is settled with the consumers; the two operations, the nine tables and the retired elements are fixed by the target architecture |
| Valuable | Unblocks the app, operations and test stories of this legacy key on Day 1 and every consumer of the clocks and the deviation flag |
| Estimable | Two documents, one additive change, three consumed operations, nine contract tables, three fakes and seven contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the clocks and the deviation flag on the case record view

  Background:
    Given the service naming rule of the platform library is in force
    Given the rwb-case event types are CaseCreated, CaseAllocated, CaseAllocationFailed, CaseTransferred, CaseStateChanged and TimerBreached
    Given the case record view contract RWB-P3-E1035-CON is published with the Case resource

  Scenario: AC1 The OpenAPI document declares the two read operations with the added fields (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-case is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares GET /cases/{caseId} with the Case resource and GET /cases/{caseId}/timers with the Timer array, both under the base /api/recovery/case/v1 and owned by rwb-case
    Then the Case resource carries deviations[] and deviationsAvailable beside prescriptionDate, stageClockStart, deviationOpen and legalHold
    Then the Timer resource carries nextStepOwnerRole, escalatedToRole, escalatedAt, nextEscalationRole and inWarning beside timerType, startedAt, expiresAt, warnAt, paused, status and escalationLevel
    Then both operations name their security right, their 2 s budget and their error responses 401, 403, 404 and 503
    Then every added property is optional in the schema, so a consumer of the previous version keeps working

  Scenario: AC2 The composed deviation object and its availability flag (new, D-RCV-60)
    Given the deviation object declared in the document
    When it is compared with the fields the S8 contract returns
    Then it carries deviationCode, raisedAt, handlerUserId, approverUserId, pausedState, contactStop, clearedAt and outcome, with approverUserId optional
    Then deviations[] is ordered by raisedAt ascending and holds the open deviations before the cleared ones of the same date
    Then deviationsAvailable is a boolean and is the only signal a consumer uses to distinguish "no deviations" from "the deviations could not be read"
    Then the document states that a false value leaves prescriptionDate, stageClockStart, deviationOpen and legalHold in place, carries an empty deviations[] and one MSG-GEN-006 entry in the section error list

  Scenario: AC3 The timer resource fixes the ordering and the five added fields (new, D-RCV-60)
    Given the Timer array declared in the document
    When its ordering and its fields are reviewed
    Then the array is ordered by expiresAt ascending and a timer without expiresAt is last, the value of expiresAt when absent Not specified in the source documents (ACR-RWB-P3-E2015-CON-AC3)
    Then nextStepOwnerRole and nextEscalationRole are role codes and not display names
    Then escalatedToRole and escalatedAt are each either empty or set, and inWarning is a boolean derived from warnAt and the business date
    Then the document states that inWarning is read from the projection and never recomputed by a consumer, and that warnAt is computed where the timer is written

  Scenario: AC4 The three consumed contracts carry their owner and the 2 s budget (new, D-RCV-60)
    Given the consumed operations of the document
    When they are compared with the Ownership Map
    Then GET /api/recovery/deviation/v1/cases/{caseId}/deviations names S8 rwb-deviation as its owner
    Then GET /api/recovery/decision/v1/decision-log?caseId={caseId} names P7 rwb-decision as its owner
    Then POST /api/recovery/access/v1/authorise names P4 rwb-access as its owner
    Then every consumed row states one hop, the 2 s timeout, the GET retry once with jitter and the breaker per downstream
    Then the S8 read path carries the ownership gap in the document until the map is corrected
    Then every failure of a consumed call maps to 401, 403, 404, 503 or the degraded shape of AC2 and never to an empty timer answer

  Scenario: AC5 The event and workflow elements are recorded, and the retired ones absent (new, D-RCV-60)
    Given the event section of the document
    When it is reviewed against the event catalogue
    Then TimerBreached is declared as event 19 on rwb.case.events.v1 with caseId as the key and no personal data field
    Then DecisionRecorded on rwb.decision-record.v1, DeviationRaised and DeviationCleared on rwb.deviation.events.v1 and RulePackageInForce on rwb.decision.events.v1 are declared as consumed or depended on by the capability, each with its owner
    Then the workflow element states that the durable timer runs inside CaseWorkflow on task queue rwb-case in namespace rwb-recovery and writes the timer projection
    Then the document declares no timer-check Schedule, no timer-check job and no TimerDue event

  Scenario: AC6 The nine contract tables are complete and the fakes match them (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then 12.6 records None and names JOB-05 as retired
    Then the three contract fakes answer the paths and payloads of 12.2 and the deviation and approver shapes of 12.1
    Then the contract tests compare each fake with the document and fail on any drift

  Scenario: AC8 Each business rule of section 8 is covered by a criterion or a guardrail test (new, D-RCV-60)
    Given the business rules BR1 to BR10 of section 8
    When each rule is compared with the criteria of this section and with the guardrail tests of section 16
    Then each of BR1 to BR10 is covered by a criterion of this section or by a guardrail or boundary test in section 16
    Then a rule that is only an architecture constraint is covered by a guardrail or boundary test and needs no criterion

  Scenario: AC9 A status change the model does not allow is refused (new, D-RCV-60)
    Given a case whose status is held in the projection
    When a status change is requested that the status model does not allow
    Then the change is refused with the response Not specified in the source documents (NEWAC-RWB-P3-E2015-CON-AC8)
    Then the case status and the timer projection are unchanged
```

These six criteria are new for the contract baseline and test the artefact only; they restate no business outcome owned by RWB-P3-E2015-APP. The wave 2 harness RWB-ITG-E2015-ITG consumes this baseline and copies none of these criteria.




### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/case/v1`; the document never declares another service's path as provided | DP-13; Architecture v5 slide 41 notes |
| BR2 | Event names are `rwb.<short>.<Event>.v1` on the topic `rwb.<short>.events.v1`, with retry and `.dlt` topics | DP-14; Template and Rules §R4 |
| BR3 | Every event carries the CloudEvents 1.0 envelope, is keyed by caseId and carries no personal data | Architecture v5 slides 42 and 43 notes; DP-09 |
| BR4 | A read declares no Idempotency-Key; a POST declares it and stores its response | Architecture v5 slide 11; DP-09 |
| BR5 | Error responses use one envelope and one message ID per condition; the business message texts are copied unchanged from the legacy story; every message is served from the message catalogue in Thai and in English (NFR-059); the Thai wording and its approver are Not specified in the source documents (GAP-1831) and stay with DL10 | Architecture v5 platform baseline; Template and Rules §R7.2 s14; Non Functional Specification v3 NFR-059 |
| BR6 | A schema change is additive within a major version; a breaking change is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR7 | The document lists only operations owned by rwb-case; a consumed operation is described as consumed, never as provided | Ownership Map v1 |
| BR8 | The timer projection is read as data: `inWarning` and the escalation fields are never recomputed by a consumer, and `warn_at` belongs to the timer story | Ownership Map ruling ASM-0078; RWB-P3-E1028-CON |
| BR9 | No timer-check Schedule, no timer-check job and no TimerDue event is declared: the clock is a durable Temporal timer inside CaseWorkflow | DP-10; Architecture v5 slides 42 and 44 |
| BR10 | No business value is fixed in the contract: the warning days, the escalation roles and the timeouts stay data or service configuration | Template and Rules §R7.2 s17 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the deviation object and the timer fields are described | In review |
| In review | Consumer sign-off | The app, operations and test stories and the S8, P7 and P4 owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1, for example a new deviation outcome code | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | Retired element reappears | The absence test of AC5 fails | In review |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-case | Owns the OpenAPI and AsyncAPI documents and the fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the Ownership Map row for the S8 read path |
| Consuming teams (app, operations, test, and the rwb-deviation, rwb-decision and rwb-access owners) | Review and sign off the parts they consume |
| Platform library owner | Owns the CloudEvents envelope, the error envelope and the naming rule this document reuses |
| Data steward | Confirms that no personal data field is declared in an event or an answer |

The per-service login name behind the document's security scheme is not part of this baseline; the document names the scheme "the rwb-case login (DP-02)".

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Case resource | The RWB-P3-E1035-CON Case resource plus `deviations[]` and `deviationsAvailable`; the existing properties are unchanged | Not specified in the source documents (DOR-RWB-P3-E2015-CON-7) |
| Deviation object | `deviationCode`, `raisedAt`, `handlerUserId`, `approverUserId`, `pausedState`, `contactStop`, `clearedAt`, `outcome`, taken from the S8 deviation fields DF-CAS-038 to DF-CAS-045 | Not specified in the source documents (DOR-RWB-P3-E2015-CON-7) |
| Timer resource | The existing `timerType`, `startedAt`, `expiresAt`, `warnAt`, `paused`, `status`, `escalationLevel` plus `nextStepOwnerRole`, `escalatedToRole`, `escalatedAt`, `nextEscalationRole`, `inWarning`, taken from `timer` DF-WRK-027 to DF-WRK-036 and DF-WRK-043 to DF-WRK-044 and from `task.owner_role` DF-WRK-023 | Not specified in the source documents (DOR-RWB-P3-E2015-CON-7) |
| Approver | `approverUserId` only, taken from `decision_log_entry.approver_user_id` DF-DEC-010 through the P7 contract, which the approval step inside DeviationWorkflow (S8) records; the P7 ApprovalWorkflow edge is an open question; the entry itself is never returned | Not specified in the source documents (DOR-RWB-P3-E2015-CON-7) |
| Event payloads | IDs, codes, dates and amounts only; no name, address, identity number or contact point | Not specified in the source documents (DOR-RWB-P3-E2015-CON-7) |

The field-level types, lengths and required flags of the added properties are settled in the baseline review; this story fixes the names, the optionality rule of AC1 and the ordering rules of AC2 and AC3.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-case (P3); base `/api/recovery/case/v1`.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| GET | `/cases/{caseId}` | Case with `prescriptionDate`, `stageClockStart`, `deviationOpen`, `legalHold`, `deviations[]` and `deviationsAvailable` | Case record R |
| GET | `/cases/{caseId}/timers` | Timer[] ordered by `expiresAt`, with the five added fields of AC3 | Case record R |

Both operations answer 401, 403, 404 and 503 with the error envelope; neither takes an Idempotency-Key.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| GET | `/api/recovery/deviation/v1/cases/{caseId}/deviations` | S8 rwb-deviation | The open and cleared deviations of the case, faked; the Ownership Map lists only the POST and the PATCH of S8, so this row carries the gap (GAP-0714; ASM-1261; open question GAP-1818, owner Solution architect) |
| GET | `/api/recovery/decision/v1/decision-log?caseId={caseId}` | P7 rwb-decision | The approver on the decision log entry of each deviation decision, faked |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The role, scope and Case record right check, faked |

Every row is one hop with a 2 s timeout, a GET retry once with jitter and a breaker per downstream.

#### 12.3 Events published

| Event | Topic | Owner | Schema element |
|---|---|---|---|
| `rwb.case.TimerBreached.v1` (event 19) | `rwb.case.events.v1` | P3 rwb-case | caseId, caseNo, timerId, timerType, expiresAt; published by the durable timer in RWB-P3-E1028-APP when it fires, consumed by gateway-bff for the officer inbox |
| `rwb.decision.DecisionRecorded.v1` (event 08) | `rwb.decision-record.v1` | P7 rwb-decision | decision record reference, ruleId, ruleVersion, finalCall, decidedAt; the local decision-record library publishes it (DP-03) |

This story declares the two elements because the capability depends on them; it publishes neither itself.

#### 12.4 Events consumed

| Event | Topic | Owner | Consumer contract element |
|---|---|---|---|
| `rwb.deviation.DeviationRaised.v1` (event 06) | `rwb.deviation.events.v1` | S8 rwb-deviation | caseId, deviationCode, raisedAt; consumed by rwb-case to pause the stage timer and set `deviation_open` |
| `rwb.deviation.DeviationCleared.v1` (event 07) | `rwb.deviation.events.v1` | S8 rwb-deviation | caseId, deviationCode, clearedAt, outcome; consumed by rwb-case to resume the stage timer |
| `rwb.decision.RulePackageInForce.v1` (event 30) | `rwb.decision.events.v1` | P7 rwb-decision | package code, version label, checksum, valid-from date; refreshes the model the timer and the case keep in force |

The three rows are consumed inside rwb-case by RWB-P3-E1028-APP; this baseline fixes their shape and their key (caseId), and the read path of this story subscribes to none of them.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| CaseWorkflow | Workflow, parent, one per case, workflow ID = case ID | `rwb-case` | Holds the durable timer, the warning point and the escalation; raises TimerBreached; the timer projection is its write |
| Timer projection | Write inside the workflow's activity | `rwb-case` | The `timer` row with `escalated_to_role` and `escalated_at`; the row the timers operation reads |

No activity is registered by this story; the two rows fix what the read path may assume about the writer.

#### 12.6 Schedules

None. The five-minute timer check (JOB-05) is retired with the TimerDue event (Architecture v5 slides 42 and 44; Ownership Map ruling ASM-0078), and this baseline registers no Schedule, no cron entry and no job name. The platform's stuck workflow scan (JOB-21) is a visibility query and is not part of this contract.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| timer | P3 (rwb_case) | The projection the timers operation reads and the timer story writes |
| recovery_case | P3 (rwb_case) | `prescription_date`, `stage_clock_start`, `deviation_open`, `legal_hold` |
| task | P3 (rwb_case) | `owner_role`, the source of `nextStepOwnerRole` |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_case | The envelope of the two event rows above; not written by the read path |

`deviation` is S8's and `decision_log_entry` is P7's; the contract names them only as consumed answers (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-deviation WireMock | `GET /cases/{caseId}/deviations` with X3 on RW-2026-000502, X1 and X3 on RW-2026-000504, X1 cleared on RW-2026-000505, an empty answer and a delayed answer beyond 2 s | App story, operations smoke profile, contract tests |
| rwb-decision WireMock | `GET /decision-log?caseId=` with entry DLE-9101 and approver U-LG-01 for X3, the X1 approvers, and a delayed answer beyond 2 s | App story, operations smoke profile, contract tests |
| rwb-access WireMock | `POST /authorise` with a granted answer, a refused answer for a role without Case record R and a refused scope over SME-NTH | App story, operations smoke profile, contract tests |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed | Case and timers provided; deviations, decision log and authorise consumed; one hop, 2 s |
| Kafka | 2 declared as published by their owners, 3 declared as consumed | TimerBreached and DecisionRecorded; DeviationRaised, DeviationCleared and RulePackageInForce |
| Temporal | 1 workflow, 1 projection write | CaseWorkflow with the durable timer; no Schedule and no activity added here |
| File | None | No file in this contract |

### 13. Solution plan

**Deliverables.** The additive change to `openapi/rwb-case-v1.yaml`, the deviation object as a shared component, the AsyncAPI fragment of `rwb.case.events.v1` that names TimerBreached, the contract README rows for the ordering, the degraded shape and the retired elements, and the three WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | The monolith base path of the legacy API (Template and Rules §R5.5, DP-13) | `/api/recovery/case/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.case.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

No pattern is claimed for the parameters contract (DP-06): this capability reads no parameter and re-applies no warning day.

**Build steps**

1. Add the deviation object and the two added properties to the Case resource; validate the additive rule of AC1 in the pipeline.
2. Add the five properties to the Timer resource and the ordering rule of AC3.
3. Write the degraded-shape rule of AC2 as a schema constraint and a README row, so a consumer cannot read an empty list as "no deviations".
4. Record the three consumed rows with their owner, their budget and the gap row of the S8 path; map every failure code.
5. Record the five event rows and the workflow row, and add the absence test for the retired job, topic and event of AC5.
6. Publish the three fakes and the seven contract tests; a drift between a fake and the document fails the build.
7. Baseline tag and the consumer sign-off note, including the S8, P7 and P4 owners and the wave 2 harness.

**Done when.** The OpenAPI and AsyncAPI artefacts validate in the pipeline, the seven contract tests pass, the three fakes answer every consumed path and the drift test is green, and the app, operations and test stories have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-030 | A response body or a query fails schema validation | The request could not be read: {detail}. |
| MSG-GEN-006 | A consumed call does not answer in time | {system} is not available. Your request is queued and will be retried. |
| MSG-P3-003 | A timer or the prescription date is inside its warning period | {timer} ends on {date}. |
| MSG-P3-004 | The case is on hold for a deviation | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-P3-018 | The case has no running, paused or expired timer | There are no running timers on this case. |
| MSG-P4-002 | A role without Case record R reads either operation | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case is outside the person's scope | This case is not in your scope. |

The message IDs are contract elements; the text is the agreed text taken from the legacy story where the message already existed, and the {system} value of MSG-GEN-006 is fixed by the consumed row that failed.

### 15. Screens and states

The contract serves SCR-03 Case record in its Loading, Read only, Editable, On hold and Degraded states, through the gateway-bff composite route (DP-19). Its empty, error and no access states are Not specified in the source documents (CG-ALL-4224). The route calls rwb-case twice and rwb-source-data once in parallel; this baseline fixes the two rwb-case answers only, and the composite route specification, the screen field list and the masking of customer fields belong to RWB-PLT-N001-CON and RWB-P3-E1035-CON.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P3-E2015-CON-01 | AC1 | Contract | The document validates; the two operations and the added properties are present and optional |
| TC-P3-E2015-CON-02 | AC2 | Contract | The deviation object's eight properties; an empty list with `deviationsAvailable` false validates and keeps the case fields |
| TC-P3-E2015-CON-03 | AC3 | Contract | The Timer ordering by `expiresAt`; the five added properties; a timer with no `expiresAt` sorts last |
| TC-P3-E2015-CON-04 | AC4 | Contract | Three consumed rows with their owner, the 2 s budget, the retry rule and the error mapping; the S8 gap row present |
| TC-P3-E2015-CON-05 | AC5 | Contract | Five event rows with their key and envelope; the workflow row; the absence test for the retired timer check, its topic and TimerDue |
| TC-P3-E2015-CON-06 | AC6 | Component | The nine sub-tables present with owners; the three fakes match the document; a drifted fake fails the build |
| TC-P3-E2015-CON-07 | AC6 | Contract | Boundary of the four tables of section 12.7: the P3 owner and contracted use of timer, recovery_case and task, and the PLT rows; no read path writes outbox_event, processed_event or idempotency_key |
| TC-P3-E2015-CON-08 | AC7 | Contract | The timer answer returns `paused`, `nextStepOwnerRole` and `escalatedAt` as the projection holds them; no consumer recomputes `inWarning`; the deviation `contactStop` and `clearedAt` come from S8 unchanged |
| TC-P3-E2015-CON-09 | AC8 | Contract | Each of BR1 to BR10 maps to a criterion or to a guardrail or boundary test; an unmapped rule fails the build |
| TC-P3-E2015-CON-10 | AC9 | Contract | A status change the model does not allow is refused and leaves the case status and the timer projection unchanged |

### 17. Guardrails

- No business value in the contract: the warning days, the escalation roles, the deviation codes and the timeouts stay data, reference data or service configuration.
- No personal data in a schema, an example or a fake: IDs, codes, dates and amounts only; `handlerUserId` and `approverUserId` are staff identifiers and no customer field is declared.
- The contract names only rwb-case tables and only operations owned by rwb-case; the S8, P7 and P4 operations are consumed and faked, never declared as provided (DP-01).
- One REST base and one topic per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- ACE data is reached only through the owner's contract or the `v_ace_*` views; this document declares no ACE view and no cross-schema join.
- No retired element is reintroduced: the absence test of AC5 fails a build that declares a timer-check Schedule, a timer-check job or a TimerDue event.
- Every example in the document is synthetic; no production payload is copied into a schema or a fake.
- The error envelope, the CloudEvents envelope and the naming rule come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-WKM-004 | A breached service level visible to the escalation role without the case moving | The escalation fields of the Timer resource and the TimerBreached event element | TC-P3-E2015-CON-03, TC-P3-E2015-CON-05 |
| REQ-WKM-005 | Timers, escalation state and the deviation flag on the case record view | The two read operations, the deviation object and the timer ordering | TC-P3-E2015-CON-01 to TC-P3-E2015-CON-03 |
| REQ-DVH-002 | A deviation pauses the stage clock and keeps the prescription clock running | `deviations[]`, `deviationsAvailable`, `prescriptionDate` and the DeviationRaised and DeviationCleared rows | TC-P3-E2015-CON-02, TC-P3-E2015-CON-05 |
| REQ-DRI-001 | Every decision writes one record holding the case, the decision, the recommendation, the approval and the outcome | `approverUserId` from the decision log and the DecisionRecorded row | TC-P3-E2015-CON-02, TC-P3-E2015-CON-04 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three consumed rows with their budget and breaker | TC-P3-E2015-CON-04 |

### 19. Out of scope

- The implementation of the two read operations, the merge, the ordering and the panels (RWB-P3-E2015-APP).
- The deployment, the consumer groups, the dashboards and the runbook (RWB-P3-E2015-OPS).
- The timer mechanism, the escalation write and the TimerBreached publication (RWB-P3-E1028-CON and RWB-P3-E1028-APP).
- The base Case resource and the case record view's other sections (RWB-P3-E1035-CON).
- The S8, P7 and P4 contracts themselves: consumed and faked, never defined here.
- The gateway-bff composite route and the screen field list (RWB-PLT-N001-CON).
- The cross-service journey harness and its evidence (RWB-ITG-E2015-ITG).

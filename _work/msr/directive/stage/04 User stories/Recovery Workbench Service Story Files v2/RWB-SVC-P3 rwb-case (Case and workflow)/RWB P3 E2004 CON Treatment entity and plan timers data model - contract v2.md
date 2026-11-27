# RWB-P3-E2004-CON Treatment entity and plan timers data model

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E2004-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-004 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement |
| Contract version | API paths under /api/recovery/case/v1; event contracts rwb.treatment.TreatmentApproved.v1 and rwb.payment.PaymentMissed.v1 (.v1); OpenAPI document version Not specified in the source documents (DOR-RWB-P3-E2004-CON-23) |
| Depends on (build) | None; platform delivery prerequisites RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1044-CON, RWB-PLT-E1047-CON, RWB-PLT-E1071-CON, RWB-PLT-E1072-CON, RWB-PLT-TE006-CON and RWB-PLT-N001-CON |
| Contract dependencies | S2 rwb-treatment treatment read; P7 rule package version and rule catalogue row (section 4 step 5; section 12.5); RWB-P3-E1042-CON and RWB-P3-E1043-CON; the P4 authorise call of the decision log right (Not specified in the source documents (GAP-2404)) |
| Integration dependencies | rwb.treatment.TreatmentApproved.v1 (rwb-treatment) and rwb.payment.PaymentMissed.v1 (rwb-payment) (section 12.4) |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-014, FR-P3-015, FR-P3-016, FR-P3-022, FR-P3-025, FR-P3-033, FR-P3-034) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-004 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (18 resolved, 39 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the case-side plan-timer seam — the two event contracts rwb-case consumes (`rwb.treatment.TreatmentApproved.v1` and `rwb.payment.PaymentMissed.v1`), the timer projection shape behind `GET /api/recovery/case/v1/cases/{caseId}/timers`, what rwb-case consumes from S2 for the treatment record and from P7 for the package version and the rule ID, the inbox dedupe and the outbox envelope, the 2 s one-hop budget, the six error codes of the journey, the nine contract tables and the contract fakes** — so that **the app, operations and test stories of this legacy key build against one fixed, testable seam on Day 1, and the treatment owner, the rule owner and the case owner can never drift on a field, an event key or a version without a failing build**.

The baseline records three target facts as contract elements, because every consumer depends on them: rwb-case holds **no treatment table** and reads the treatment only through the S2 contract (Ownership Map `treatment`; Architecture v5 slides 18 and 41); the `timer` row is a **projection** behind the timers operation while the clock is a **durable Temporal timer inside CaseWorkflow** (Ownership Map `timer` ruling ASM-0078; Architecture v5 slides 42 and 44); and the DP04 treatment product is **P1's read-only copy built from events**, with no data lake (Ownership Map `dp_treatment` ruling ASM-0080; DP-17; ADR-018).

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling rule (DP-11; ADR-020), and local evaluation with a local decision record is the rules and audit rule (DP-04, DP-03; ADR-017, ADR-022). Both only work if the seam is written down once. The seam of RWB-E2-004 is small and load-bearing: one event that announces an approved treatment, one event that reports a missed installment, one projection shape that two readers sort the same way, one treatment read, one rule-and-version read, and one decision that has to be recorded before the case moves.

The ownership move makes the baseline the only place where the split can be seen at once. The legacy story held the treatment record, its timers, the rule evaluation and the extract inside one module. In the target the treatment is S2's, the package version and the rule rows are P7's, the DP04 copy is P1's, the durable-timer behaviour is the platform kit's and the case state, the projection and the route move are rwb-case's. A field renamed on the S2 side empties the plan panel; an event keyed on the treatment instead of the case breaks the per-case ordering of the case router; a `treatmentId` that is dropped from the timers answer leaves the officer unable to tie a due date to a plan; and a decision record written after the state change breaks the audit chain.

The baseline also stops the legacy mechanism leaking back in. `TimerScheduler`, its Quartz implementation JOB-05 and the TimerDue event are retired (DP-10; Architecture v5 slides 42 and 44; ASM-0078), so no contract in this story declares a timer-check job, a timer-check topic, a Schedule or a `timer` row that anything but the plan-timer step of CaseWorkflow may write. Naming is fixed the same way: schema `rwb_case`, base `/api/recovery/case/v1`, topic `rwb.case.events.v1`, event names `rwb.case.<Event>.v1`, task queue `rwb-case` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.case`.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL; RWB-PLT-E1047-CON), so the base, the topic and the event names follow the platform rule and not a local choice (DP-13, DP-14).
- The CloudEvents 1.0 envelope, the platform error envelope, the retry and `.dlt` topic convention and the outbox and inbox library are the platform baseline (RWB-PLT-EVT; RWB-PLT-TE006-CON; DP-09); where this document narrows them it says so.
- The parameters and reference-data contracts of rwb-case are published (RWB-PLT-E1042-CON, RWB-P3-E1042-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON), so CURE_PERIOD_DAYS and `plan.warn-days` are named as data and never as values, and LOV-TIMER and LOV-TIMER-STATUS are closed lists whose values are fixed in the schema enums (DP-06, DP-07).
- The local decision-record library is published (RWB-PLT-E1027-CON; DP-03) and the embedded Drools kit contract is published (RWB-PLT-E1072-CON; DP-04), so `RuleResult` and `NoPackageInForce` are the kit's elements and this story reuses them.
- The timer contract RWB-P3-E1028-CON is published, so the Timer resource this story extends with the plan fields has one owner document.
- The case record contract RWB-P3-E1018-CON is published, so the Case resource that carries `routeState` and `ruleVersion` has one owner document.
- The consumed operations and their owners come from the Ownership Map only; this document declares no other service's operation as provided and no path that the map does not carry.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the additive change to the rwb-case OpenAPI 3.1 document: the plan-timer fields on the Timer resource and `routeState` with `ruleVersion` on the Case resource.
2. Fix the ordering rule of the timers answer for plan timers, so a plan timer and a stage timer sort by the same key and two readers never differ.
3. Publish the two consumed event contracts with their CloudEvents attributes, their key, their payload, their retry and `.dlt` behaviour and their inbox dedupe rule.
4. Publish the outbox envelope and the published CaseStateChanged payload, with the rule ID, the version and the decision record reference it carries.
5. Record what rwb-case consumes from S2 (the treatment read) and from P7 (the package version in force and the rule catalogue row), with the 2 s budget and the failure behaviour of each.
6. Map the six message IDs of the journey to their conditions, their operation and their substituted values, and state that no consumer re-words a message.
7. Publish the nine contract tables of section 12 and the five contract fakes.
8. Add the contract tests: schema validation, the ordering rule, the event envelope and key, the dedupe rule, the 2 s budget, the error mapping, the absence of every retired element, and the drift between a fake and the document.
9. Tag the baseline and hand it to RWB-P3-E2004-APP, RWB-P3-E2004-OPS and RWB-ITG-E2004-ITG.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body or an event payload fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the error envelope | MSG-GEN-001 | AC1, AC2 |
| X2 | A consumed event carries no CloudEvents `id`, no case key or no treatment ID | The consumer refuses it and routes it to `.dlt`; no timer and no record result | MSG-P3-005 | AC1, AC4 |
| X3 | A field is renamed or removed inside major version 1 | The contract test fails; the change needs a new major version and a consumer sign-off | None | AC2, AC6 |
| X4 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X5 | A retired element — a treatment table in `rwb_case`, a JOB-05 Schedule, a TimerDue topic or a data-lake extract — reappears in the document or a job | The absence test fails | None | AC7 |
| X6 | A field-level definition is missing from the source material | The element carries the placeholder and one gap row | None | AC2, AC3 |
| X7 | A consumed owner answers outside the 2 s budget, or answers 5xx | The step fails with the retry policy of the kit and a breaker per downstream; no partial write is contracted | MSG-P7-003 | AC5 |
| X8 | The rule package has no version in force on the business date | The contract states that `NoPackageInForce` is a non-retryable outcome, not an error code of the API | MSG-P3-027 | AC3, AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the two same-service contracts it extends and the Ownership Map only |
| Negotiable | Field-level detail is settled with the consuming and producing owners; the two events, the projection shape, the retired elements and the nine tables are fixed by the target architecture |
| Valuable | Unblocks the app, operations and test stories of this legacy key on Day 1, plus the wave 2 harness that drives the same seam |
| Estimable | One additive document change, two consumed event contracts, one published envelope, five consumed operations, nine contract tables and five fakes |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact — the schema, the event payload, the table, the fake — never against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the case-side plan-timer seam

  Background:
    Given the service naming rule and the CloudEvents 1.0 envelope of the platform library are in force
    Given the rwb-case event types are CaseCreated, CaseAllocated, CaseAllocationFailed, CaseTransferred, CaseStateChanged and TimerBreached
    Given the timer contract RWB-P3-E1028-CON and the case record contract RWB-P3-E1018-CON are published

  Scenario: AC1 The two consumed event contracts are fixed (new, D-RCV-60)
    Given the event section of the document
    When the two consumed event contracts are reviewed
    Then rwb.treatment.TreatmentApproved.v1 is declared on rwb.treatment.events.v1, owned by S2 rwb-treatment as event 10, keyed by caseId, with the attributes id, source, type, specversion, time, subject and datacontenttype
    Then its payload carries treatmentId, caseId, treatmentType, approvalLevel, decisionLogId, firstDueDate, installments and offerAmount, and no name, address, identity number or contact point
    Then rwb.payment.PaymentMissed.v1 is declared on rwb.payment.events.v1, owned by P8 rwb-payment as event 12, keyed by caseId, with treatmentId, dueDate, amountDue and businessDate
    Then the document states that the case router dedupes on the CloudEvents id through the inbox of schema rwb_case and turns each event into a signal on CaseWorkflow
    Then a message without an id, without a case key or without a treatment ID is refused and routed to .dlt with its retry topic

  Scenario: AC2 The timer projection behind the timers operation is fixed (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-case with this change
    When it is validated against the OpenAPI 3.1 schema
    Then GET /cases/{caseId}/timers is declared under the base /api/recovery/case/v1, owned by rwb-case, with the security right, the 2 s budget and the responses 401, 403, 404 and 503
    Then each plan Timer carries timerType INSTALLMENT_DUE or CURE_PERIOD, treatmentId, startedAt, expiresAt, warnAt, paused and status, beside the fields of RWB-P3-E1028-CON
    Then the array is ordered by expiresAt ascending and a timer without expiresAt is last, for plan timers and stage timers alike
    Then every added property is optional in the schema, so a consumer of the previous version keeps working
    Then the field-level types, lengths and required flags are Not specified in the source documents (GAP-0705; ASM-1252) and are fixed in the baseline review

  Scenario: AC3 What rwb-case consumes from S2 and P7 is fixed (new, D-RCV-60)
    Given the consumed operations of section 12.2
    When they are compared with the Ownership Map
    Then GET /api/recovery/treatment/v1/treatments/{treatmentId} names S2 rwb-treatment as its owner and returns the type, terms, installments, offer amount, approval level, decisionLogId, firstDueDate and bookedAt of the treatment
    Then GET /api/recovery/decision/v1/rule-catalog/{ruleId}?packageVersion= names P7 rwb-decision as its owner and returns actionText, ownerRole, timerSpec and outputs for R-RES-25 and R-RES-27
    Then GET /api/recovery/decision/v1/decision-log/{entryId} names P7 rwb-decision as its owner and returns the approval entry and its approverUserId only
    Then the document states that the rule is evaluated by the embedded Drools kit inside the EvaluateRules activity of rwb-case, under the package version rwb-decision has in force, and that NoPackageInForce is non-retryable
    Then no treatment row, no treatment column and no key into rwb_treatment is declared in the rwb-case contract

  Scenario: AC4 The outbox envelope and the published case event are fixed (new, D-RCV-60)
    Given the published part of the document
    When it is reviewed
    Then rwb.case.CaseStateChanged.v1 is declared as event 05 on rwb.case.events.v1, keyed by caseId, with caseId, caseNo, fromState, toState, ruleId, ruleVersion, decisionRecordId and occurredAt
    Then it is written to outbox_event in the same local transaction as the timer row and the route state, and relayed to Kafka by the outbox relay
    Then rwb.decision.DecisionRecorded.v1 on rwb.decision-record.v1 is declared as published by the local decision-record library of DP-03 with ruleId, ruleVersion, finalCall and decidedAt
    Then the document states that no event is published for the timer expiry, because TimerDue has no topic and the expiry stays a fact of the workflow history
    Then it declares no personal data field in either event

  Scenario: AC5 The one-hop budget and the error codes are fixed (new, D-RCV-60)
    Given the consumed rows of section 12.2 and the message table of section 14
    When they are reviewed
    Then every consumed row states one hop, the 2 s timeout, the GET retry once with jitter and the breaker per downstream
    Then MSG-GEN-001, MSG-GEN-003, MSG-P3-005, MSG-P3-027, MSG-P7-003 and MSG-P1-001 each name the condition, the operation or the step that raises it and the values it substitutes
    Then a failure of a consumed call maps to 401, 403, 404, 503 or the message of its own row, and never to an empty timer answer
    Then the document states that no consumer re-words a message text and that the substituted values name fields, states, package codes, business dates and products only

  Scenario: AC6 The nine contract tables are complete and the fakes match them (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then 12.1 names only GET /cases/{caseId} and GET /cases/{caseId}/timers, both owned by rwb-case
    Then 12.6 records None and names JOB-05 retired
    Then the five contract fakes answer the paths and payloads of 12.2 and 12.4, and the contract tests fail on any drift between a fake and the document

  Scenario: AC7 The retired elements are absent from the document (new, D-RCV-60)
    Given the published document, its AsyncAPI fragment and its job declarations
    When the absence test runs
    Then no treatment table, treatment column or rwb_treatment key is declared in schema rwb_case
    Then no timer-check Schedule, no timer-check task queue, no JOB-05 entry and no TimerDue event or topic is declared
    Then no data-lake, Power BI or extract operation is declared by rwb-case, and the DP04 product is declared only as consumed from P1
    Then the absence test fails a build that declares any of them
```

These seven criteria are new for the contract baseline and test the artefact only; they restate no business outcome owned by RWB-P3-E2004-APP. The wave 2 harness RWB-ITG-E2004-ITG consumes this baseline and copies none of these criteria.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/case/v1`; the document never declares another service's path as provided | DP-13; Architecture v5 slide 41 notes |
| BR2 | Event names are `rwb.<short>.<Event>.v1` on `rwb.<short>.events.v1`, with retry and `.dlt` topics | DP-14; Template and Rules §R4 |
| BR3 | Every event carries the CloudEvents 1.0 envelope, is keyed by caseId and carries no personal data | Architecture v5 slides 42 and 43 notes; DP-09 |
| BR4 | A read declares no Idempotency-Key; a POST declares it and stores its response | Architecture v5 slide 11; DP-09 |
| BR5 | The `timer` row is a projection and the clock is a durable timer inside CaseWorkflow; no Schedule, no job and no TimerDue event is declared | DP-10; Architecture v5 slides 42 and 44; ASM-0078 |
| BR6 | `rwb_case` holds no treatment table and no key into `rwb_treatment`; the treatment is consumed through the S2 contract only | DP-01; ASM-0078; Architecture v5 slides 18 and 41 |
| BR7 | The treatment data product is P1's read-only copy built from events; no data lake and no extract is declared by this service | DP-17; ADR-018; ASM-0080 |
| BR8 | The decision record is written before the timer and the route state, and the contract carries the rule ID and the package version on every record | DP-03; Principle 5; R-UNI-39 |
| BR9 | `NoPackageInForce` is a non-retryable outcome of the kit, not an HTTP error code of the case API | DP-04; D-RCV-36 T7 |
| BR10 | A schema change is additive within a major version; a breaking change is a new major version with consumer sign-off | Architecture v5 slide 42 notes (BACKWARD compatibility) |

Each rule BR1 to BR10 is checked by TC-P3-E2004-CON-09 (section 16).

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two events, the projection shape, the consumed rows and the nine tables are described | In review |
| In review | Consumer sign-off | The app, operations and test stories, and the S2, P8, P7 and P1 owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1, for example a new timer field | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped, or an event key changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | Retired element reappears | The absence test of AC7 fails | In review |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-case | Owns the OpenAPI and AsyncAPI documents and the fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and any change to the projection or the retired-element list |
| The S2, P8, P7 and P1 owners | Own the consumed operations and events and sign off the shapes taken from their documents |
| Consuming teams (app, operations, test, and the harness) | Review and accept the parts they consume |
| Platform library owner | Owns the CloudEvents envelope, the error envelope, the outbox and inbox library and the naming rule this document reuses |
| Data steward | Confirms that no personal data field is declared in an event or an answer |

The per-service login name behind the document's security scheme is not part of this baseline; the document names the scheme "the rwb-case login (DP-02)".

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Timer resource | The RWB-P3-E1028-CON fields plus `treatmentId` for the plan timers; types INSTALLMENT_DUE and CURE_PERIOD come from LOV-TIMER and statuses from LOV-TIMER-STATUS | Not specified in the source documents (DOR-RWB-P3-E2004-CON-7) |
| Case resource | The RWB-P3-E1018-CON Case resource plus `routeState` (BOOKED_IN_ALS_NLEADS, PLAN_RUNNING, PLAN_CURE_PERIOD) and `ruleVersion` | Not specified in the source documents (DOR-RWB-P3-E2004-CON-7) |
| Treatment answer | `treatmentId`, `caseId`, `treatmentType`, `approvalLevel`, `decisionLogId`, `firstDueDate`, `installments`, `offerAmount`, `bookedAt`; taken from DF-TRT-001 to DF-TRT-014 and DF-TRT-029 through the S2 contract | Not specified in the source documents (DOR-RWB-P3-E2004-CON-7) |
| Rule and version answer | `ruleId`, `packageVersion`, `actionText`, `ownerRole`, `timerSpec`, `outputs`; taken from DF-REF-002, DF-REF-003, DF-REF-296 and DF-REF-298 through the P7 contract | Not specified in the source documents (DOR-RWB-P3-E2004-CON-7) |
| Decision record | `ruleId`, `ruleVersion`, `finalCall`, `decidedAt`, `decisionRecordId`; the approval entry's `approverUserId` (DF-DEC-010) is read only; it is personal data and is carried in no event payload and no record this service writes | Not specified in the source documents (DOR-RWB-P3-E2004-CON-7) |
| Event payloads | IDs, codes, dates, versions and amounts only; no name, address, identity number or contact point | Not specified in the source documents (DOR-RWB-P3-E2004-CON-7) |
| DP04 product | Read as published by P1: the treatment link and the derived status; no field of it is declared as this service's | Not specified in the source documents (DOR-RWB-P3-E2004-CON-7) |

The field-level types, lengths and required flags of the added properties are settled in the baseline review; this story fixes the names, the optionality rule of AC2 and the ordering rule of AC2.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-case (P3); base `/api/recovery/case/v1`. Both operations are already in the Ownership Map and this baseline extends them; no new path is declared.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| GET | `/cases/{caseId}/timers` | Timer[] ordered by `expiresAt`, with the plan fields `treatmentId`, `timerType` INSTALLMENT_DUE or CURE_PERIOD, `startedAt`, `expiresAt`, `warnAt`, `paused` and `status` | Case record R, scope applied |
| GET | `/cases/{caseId}` | Case with `routeState` and `ruleVersion` beside its status, queue and clocks | Case record R, scope applied |

Both answer 401, 403, 404 and 503 with the error envelope; neither takes an Idempotency-Key.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| GET | `/api/recovery/treatment/v1/treatments/{treatmentId}` | S2 rwb-treatment | The treatment type, terms, installments, offer amount, approval level, decision log entry, first due date and booked at; faked |
| GET | `/api/recovery/decision/v1/decision-log/{entryId}` | P7 rwb-decision | The approval entry and its approver, before the first move; faked |
| GET | `/api/recovery/decision/v1/rule-catalog/{ruleId}?packageVersion=` | P7 rwb-decision | The action text, owner role, timer spec and outputs of R-RES-25 and R-RES-27; faked |
| GET | `/api/recovery/source-data/v1/data-products/DP04/records` | P1 rwb-source-data | The DP04 treatment rows of a business date and their staleness; the read path and the freshness element carry the gap (GAP-0704; ASM-1251) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The role, scope and Case record right check; faked |

Every row is one hop with a 2 s timeout, a GET retry once with jitter and a breaker per downstream (DP-11; ADR-020).

#### 12.3 Events published

| Event | Topic | Owner | Schema element |
|---|---|---|---|
| `rwb.case.CaseStateChanged.v1` (event 05) | `rwb.case.events.v1` | P3 rwb-case | caseId, caseNo, fromState, toState, ruleId, ruleVersion, decisionRecordId, occurredAt; outbox in the same transaction as the state change |
| `rwb.decision.DecisionRecorded.v1` (event 08) | `rwb.decision-record.v1` | P7 rwb-decision owns the topic; the local decision-record library of DP-03 publishes it from rwb-case | decision record reference, ruleId, ruleVersion, finalCall, decidedAt |

This story declares the two elements because the plan step depends on them; it publishes neither itself. No event is declared for the timer expiry, because TimerDue is retired and the expiry stays a fact of the workflow history.

#### 12.4 Events consumed

| Event | Topic | Owner | Consumer contract element |
|---|---|---|---|
| `rwb.treatment.TreatmentApproved.v1` (event 10) | `rwb.treatment.events.v1` | S2 rwb-treatment | treatmentId, caseId, treatmentType, approvalLevel, decisionLogId, firstDueDate, installments, offerAmount; key caseId; inbox dedupe on `id`; starts the plan-timer step |
| `rwb.payment.PaymentMissed.v1` (event 12) | `rwb.payment.events.v1` | P8 rwb-payment | treatmentId, dueDate, amountDue, businessDate; key caseId; inbox dedupe; starts the cure-period step |

Both are consumed by the case router of rwb-case, which dedupes through the inbox of schema `rwb_case` and calls `signalWithStart` on CaseWorkflow. `rwb.decision.RulePackageInForce.v1` (event 30) is consumed by RWB-P3-E2042-APP into the model cache and is declared here only as a dependency of the version this baseline names.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| CaseWorkflow | Workflow, parent, one per case, workflow ID = case-{caseId} | `rwb-case` | Holds the plan-timer step and the durable INSTALLMENT_DUE and CURE_PERIOD timers; its history carries the timer-due fact; Continue-As-New at every stage end and at least every 28 days |
| PlanTimerStep | Activity | `rwb-case` | Input: caseId, treatmentId, businessDate. Output: timerId, timerType, expiresAt, ruleId, ruleVersion; writes the local decision record, the projection, the route state and the outbox row in one local transaction |
| EvaluateRules | Activity (workflow kit) | `rwb-case` | Input: packageCode, facts, businessDate. Output: `RuleResult(packageCode, packageVersion, ruleId, outputs)`; raises `NoPackageInForce`, non-retryable |
| RecordAndApply | Activity (workflow kit) | `rwb-case` | Input: the decision record, the timer row, the route state and the outbox rows; one transaction, no partial write |

No activity is registered by this story; the four rows fix what a consumer and a test may assume about the writer.

#### 12.6 Schedules

None. The five-minute timer check JOB-05 is retired with the TimerDue event (Architecture v5 slides 42 and 44; ASM-0078), and this baseline registers no Schedule, no cron entry and no job name. The 01:30 extract JOB-15 that loads the DP04 copy is P9 rwb-reporting's under the bank Airflow (Architecture v5 slide 44) and is declared here only as the owner of the data the DP04 read returns; the platform's stuck workflow scan JOB-21 is a visibility query and is not part of this contract.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| timer | P3 (rwb_case) | The projection the timers operation reads and the plan-timer step writes, including `treatment_id` (DF-WRK-042) |
| recovery_case | P3 (rwb_case) | `route_state` (DF-CAS-007) and `rule_version` (DF-CAS-021) of the plan move |
| task | P3 (rwb_case) | `owner_role` of the next step a plan timer carries |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_case | The envelope of the published row and the dedupe of the two consumed rows (DP-09) |

`treatment` is S2's in `rwb_treatment` and `dp_treatment` is P1's in `rwb_source_data`; the contract names them only as consumed answers. `rwb_case` holds no foreign key into another schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-treatment WireMock | `GET /treatments/{treatmentId}` for T-0401 and T-0402, the refusal answers of the invalid plans and the closed case; `rwb.treatment.TreatmentApproved.v1` for the same treatments including a duplicate id | App story, operations smoke profile, contract tests | 
| rwb-decision WireMock | `GET /decision-log/{entryId}` with DLE-9001 and U-APR-01 and a 404 for DLE-0000; `GET /rule-catalog/{ruleId}?packageVersion=` for R-RES-25 and R-RES-27 at RES-2026.12; a no-version answer and a delayed answer beyond 2 s | App story, operations smoke profile, contract tests |
| rwb-payment WireMock | `rwb.payment.PaymentMissed.v1` for due date 2026-12-31 on business date 2027-01-01, and its absence before the due date | App story, contract tests |
| rwb-source-data WireMock | `GET /data-products/DP04/records` with ten rows for 2026-12-01 (eight APPROVED, two BOOKED) and the stale answer with MSG-P1-001 | App story, contract tests |
| rwb-access WireMock | `POST /authorise` with a granted answer, a refused answer for a role without Case record R and a refused scope | App story, contract tests |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 5 consumed | Case and timers provided; treatment, decision log, rule catalogue, DP04 records and authorise consumed; one hop, 2 s |
| Kafka | 2 declared as published by their owners, 2 declared as consumed | CaseStateChanged and DecisionRecorded; TreatmentApproved and PaymentMissed |
| Temporal | 1 workflow, 3 activities, no Schedule | CaseWorkflow with the plan-timer step, the EvaluateRules and RecordAndApply activities, and the durable plan timers |
| File | None | No file in this contract |

### 13. Solution plan

**Deliverables.** The additive change to `openapi/rwb-case-v1.yaml` (the plan fields on the Timer resource, `routeState` and `ruleVersion` on the Case resource), the AsyncAPI fragment of `rwb.case.events.v1` that names CaseStateChanged, the two consumed event contracts, the contract README rows for the ordering rule, the dedupe rule and the retired elements, and the five WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.case.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 adds nothing here: the contract declares no ACE view, because the case facts are `rwb_case`'s own and the treatment arrives through the S2 contract. DP-15 resolves to no migration for this story, because the baseline owns no schema; the plan projection column that DP-15 provisions belongs to RWB-P3-E2004-APP. The same-service CON baselines RWB-P3-E1028-CON and RWB-P3-E1018-CON are class H dependencies of the app story and are not DP rows.

**Build steps**

1. Add `treatmentId` to the Timer resource and the two Case properties; validate the additive rule of AC2 in the pipeline.
2. Write the ordering rule of AC2 as a schema constraint and a README row, so a plan timer and a stage timer sort the same way.
3. Write the two consumed event contracts of AC1 with their envelope, key, payload, retry and `.dlt` behaviour and the inbox dedupe rule; add the refusal rule for a message without an id, a case key or a treatment ID.
4. Write the published envelope of AC4 and the statement that the expiry publishes no event.
5. Record the five consumed rows with their owner, their budget and the DP04 gap; map every failure code to the six messages of section 14.
6. Record the four workflow and activity rows and the absence test of AC7 for the retired job, topic, Schedule and treatment object.
7. Publish the five fakes and the seven contract tests; a drift between a fake and the document fails the build.
8. Baseline tag and the consumer sign-off note, including the S2, P8, P7, P1 and P4 owners and the wave 2 harness.

**Done when.** The OpenAPI and AsyncAPI artefacts validate in the pipeline, the seven contract tests pass, the five fakes answer every consumed path and payload, the absence test fails a build that declares JOB-05, a TimerDue topic or a treatment object in `rwb_case`, and the app, operations and test stories have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field or the decision log entry is missing | Enter {field}. |
| MSG-GEN-003 | The first due date is before the proposed date | {field} cannot be before {other}. |
| MSG-P3-005 | The case is closed, or not in the state the rule expects | This case cannot move to {state} from {current}. |
| MSG-P3-027 | No RESTRUCTURE version is in force | The rule version was refused at the {check} check: {detail}. |
| MSG-P7-003 | The decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The treatment data product is stale | {product} is from {date}. Today's load has not arrived. |
| MSG-P4-002 | A role without Case record R calls an operation | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case is outside the person's scope | This case is not in your scope. |

The message IDs are contract elements; the text is the agreed text of the legacy story where the message already existed, and this baseline adds no wording. The {check} value of MSG-P3-027 is "no package in force" and its {detail} names the package code and the business date only; MSG-P1-001 names the product and the business date of the last load only.

### 15. Screens and states

The contract serves SCR-03 Case record in its Loading, Read only and Degraded states through the gateway-bff composite route (DP-19). Its empty, error and no access states are Not specified in the source documents (CG-ALL-4021). The plan timers and the route state are read from the two answers of §12.1. This baseline fixes those two answers only; the composite route path, its merge order and the screen field list belong to RWB-PLT-N001-CON, RWB-P3-E1018-CON and RWB-P3-E2015-APP. No screen and no state is added by this story.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P3-E2004-CON-01 | AC1 | Contract | The two consumed events with their envelope, key and payload; a message without an id, a case key or a treatment ID is refused to `.dlt` |
| TC-P3-E2004-CON-02 | AC2 | Contract | The document validates; the plan fields are present and optional; a timer without `expiresAt` sorts last; the uncovered field-level detail carries the placeholder |
| TC-P3-E2004-CON-03 | AC3 | Contract | The S2 and P7 consumed rows with their owner and shape; the evaluation statement; the absence of any treatment object in `rwb_case` |
| TC-P3-E2004-CON-04 | AC4 | Contract | CaseStateChanged and DecisionRecorded declared with their payload and key; the expiry publishes no event; no personal data field |
| TC-P3-E2004-CON-05 | AC5 | Contract | Five consumed rows with one hop, the 2 s budget, the retry rule and the error mapping; the six message IDs with their substituted values |
| TC-P3-E2004-CON-06 | AC6 | Component | The nine sub-tables present with owners; 12.1 names only the two rwb-case operations; 12.6 is None; the five fakes match the document |
| TC-P3-E2004-CON-07 | AC7 | Component | The absence test for the treatment object, any legacy batch job entry, the TimerDue topic, the timer-check Schedule and the data-lake extract |
| TC-P3-E2004-CON-08 | AC6 | Component | Boundary of the section 12.7 tables: each table once with its owner; no table or key of another schema is named |
| TC-P3-E2004-CON-09 | BR1 to BR10 (section 8) | Contract | Each rule of section 8 checked against the contract text and its named source |

### 17. Guardrails

- No business value in the contract: the cure period, the warning days, the timer types and the escalation roles stay parameters, reference data or package rows.
- No personal data in a schema, an example or a fake: IDs, codes, dates, versions and amounts only.
- The contract names only rwb-case tables and only operations owned by rwb-case; every other operation and event is consumed and faked, never declared as provided (DP-01).
- One REST base and one topic per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- No retired element is reintroduced: the absence test of AC7 fails a build that declares a treatment table in `rwb_case`, a timer-check Schedule, a JOB-05 entry or a TimerDue event.
- The `timer` row is declared as a projection and never as the clock; a document that implies a polling check or a scheduler row fails the review (BR5).
- Every example and fixture is synthetic; no production treatment, case, payload or version label is copied into a schema or a fake.
- The envelope, the naming rule, the outbox and inbox library and the kit elements come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-CHO-006 | A treatment record for every offer with type, terms, approval and outcome | The S2 treatment read, its fields and the treatment object's absence from `rwb_case` | TC-P3-E2004-CON-03, TC-P3-E2004-CON-07, TC-P3-E2004-CON-08 |
| REQ-CHO-007 | Plan timers run from the treatment; a missed payment raises an event | The two consumed events, the plan Timer fields and the CaseStateChanged envelope | TC-P3-E2004-CON-01, TC-P3-E2004-CON-02, TC-P3-E2004-CON-04 |
| REQ-RDF-014 | Stage 2 data products for plans and treatments exist before the first treatment | The DP04 consumed row and its staleness element | TC-P3-E2004-CON-03, TC-P3-E2004-CON-05 |
| REQ-CWC-011 | Warning thresholds and escalation targets are data and a breach raises an event without moving the case | `warnAt` on the plan Timer, declared as data read from the parameters and reference contracts | TC-P3-E2004-CON-02, TC-P3-E2004-CON-06 |
| ADR-016 | Reusable Temporal layer; Schedules replace Quartz | The workflow rows and the absence of a Schedule, a JOB-05 entry and a TimerDue event | TC-P3-E2004-CON-06, TC-P3-E2004-CON-07 |
| ADR-018 | No data lake; rwb-reporting read model from events | The DP04 row as a consumed product and the absence of any extract or data-lake element | TC-P3-E2004-CON-07 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The five consumed rows with their budget and breaker | TC-P3-E2004-CON-05 |

### 19. Out of scope

- The implementation of the plan-timer step, the projection, the route moves and the two read answers (RWB-P3-E2004-APP).
- The deployment, the consumer groups, the dashboards and the runbook (RWB-P3-E2004-OPS).
- The treatment entity and its own contract (S2; RWB-S2-E2004-APP).
- The package registry, the version in force and the rule catalogue rows (P7; RWB-P7-E2042-APP).
- The DP04 copy, its 01:30 load and its freshness stamps (P1 rwb-source-data; P9 rwb-reporting).
- The timer resource and the stage clocks this document extends (RWB-P3-E1028-CON) and the case resource it extends (RWB-P3-E1018-CON).
- The gateway-bff composite route and the screen field list (RWB-PLT-N001-CON).
- The cross-service journey harness and its evidence (RWB-ITG-E2004-ITG).

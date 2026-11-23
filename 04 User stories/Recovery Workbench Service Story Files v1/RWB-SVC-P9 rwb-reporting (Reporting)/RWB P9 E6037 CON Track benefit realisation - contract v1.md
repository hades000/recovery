# RWB-P9-E6037-CON Track benefit realisation - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P9-E6037-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-reporting |
| Service epic | RWB-SVC-P9 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-037 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P9 rwb-reporting v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the contract baseline of RWB-E6-037 for rwb-reporting — the additive change to `GET /reports/measures` that carries the benefit-realisation comparison, the variance rule, the freshness header and the nine contract tables — is split from the behaviour (RWB-P9-E6037-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract of the benefit-realisation view as rwb-reporting serves it — `GET /api/recovery/reporting/v1/reports/measures` with its period, its `baselineDate` and its filters, the measure row with `value`, `baselineValue`, `variance`, `variancePercent`, `definitionVersion`, `isBaseline` and `frozen`, the `X-Data-As-Of` header and the stale flag, the variance rule, the error envelope with its message codes, the right each answer requires, the consumed readiness answer, the nine contract tables and the contract fakes**, so that **the app story of this legacy key builds against a fixed, testable contract on Day 1, and a baseline value, a variance or a definition version can never be computed one way in the service and read another way on the screen**.

The legacy key is moved with no business change: the measures, the baseline, the monthly cadence, the record with the rule version and the refusal when the record cannot be written are the ones RWB-E6-037 fixes. What this story adds is the contract form of them: one document owner, one shape per answer, one variance rule, one order, one error envelope and one fake per consumed answer.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The measure answer is the most-consumed read surface of rwb-reporting: the steering dashboard SCR-37, the benefit section of the same screen, the Power BI refresh through the extract hand-over and the audit sample all read the same rows. Three things drift silently if no contract holds them: which baseline a value is compared with, how the variance and its percentage are computed, and which definition version a month was produced under. A baseline date that a consumer chooses for itself turns one benefit number into two; a variance computed at the edge rather than in the owner means the screen and the report disagree.

The baseline also fixes the naming the checks require: schema `rwb_reporting`, REST base `/api/recovery/reporting/v1`, topic `rwb.reporting.events.v1`, task queue `rwb-reporting` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.reporting`. It records that this read path writes nothing and publishes no event type, that the local decision record of a tracked month is the only write of the capability (DP-03), and that the ACE data products behind a measure are reached through rwb-source-data's answer and never through a view of this service (DP-05).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL), so the document, topic and event names follow the platform rule rather than a local choice.
- The platform error envelope and the CloudEvents 1.0 envelope are the platform baseline (RWB-PLT-EVT); where this document narrows them it does so explicitly.
- RWB-P9-E1013-CON is published, so `measure_definition` and `measure_snapshot` and the six baseline measures of definition version "MD-2026.11" have one owner document and the fields this story extends are an additive change to it.
- RWB-P9-E2009-CON is published, so `GET /reports/measures`, its `dimension` and `baselineValue` fields and the `X-Data-As-Of` header already have an owner document and the fields this story adds are declared against it.
- The decision-record library RWB-PLT-E1027-CON is published, so the record of a tracked month has one contract and this document declares it as consumed (DP-03).
- The gateway-bff composite route RWB-PLT-N001-CON is published, so the consumer of the answer composes SCR-37 at the edge (DP-19).
- The Ownership Map gives `GET /reports/measures` to P9 rwb-reporting; this document declares no other service's operation as provided and names no operation the map does not already give P9.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7) and sits in contract group `CG-W4`.

### 4. Flow

1. Draft the additive change to the rwb-reporting OpenAPI 3.1 document for the one read operation: the `baselineDate` parameter, the four added row properties and the stale flag.
2. Fix the variance rule in the document — value less baseline value, and the percentage over a non-zero baseline value — so no consumer computes its own (GAP-2580; ASM-4256).
3. Fix the period rule: `from` and `to` name the first and last day of the month asked for, `baselineDate` names the frozen baseline and defaults to the baseline of the definition version in force, and the period of the answer is stated once (GAP-2580; ASM-4259).
4. Fix the row order and state that the answer is one bounded array with no paging in major version 1, the ceiling being a platform parameter (GAP-2580; ASM-4257).
5. Declare that the document publishes no event type and subscribes to none, and name the local decision record as the one write of the capability (GAP-2580; ASM-4258).
6. Record the consumed readiness element with its owner, its use and its failure mapping; record that no REST operation is consumed.
7. Map every failure to the error envelope and a message ID, with the legacy texts unchanged.
8. Publish the nine contract tables of section 12 and the contract fakes; every fake answers the document and fails the build when it drifts.
9. Tag the baseline and hand it to RWB-P9-E6037-APP, to the dashboard and to the audit consumers of the answer.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the platform error envelope | None | AC1 |
| X2 | A field is renamed, retyped or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC9 |
| X4 | `from` is after `to` | 422 with MSG-GEN-003 naming the two fields | MSG-GEN-003 | AC5 |
| X5 | A required parameter is empty | 422 with MSG-GEN-001 naming the field | MSG-GEN-001 | AC5 |
| X6 | `baselineDate` names a date with no frozen baseline | 200 with the rows of the month and no variance, the row flagged as having no baseline; never an error and never a guess | None | AC4 |
| X7 | A caller reads a month outside its scope | 200 with the rows of its scope only; a scope that excludes every row answers an empty array, not an error | None | AC6 |
| X8 | The readiness answer does not arrive inside the budget | The stale flag and the header are omitted, no row is dropped and no value changes | None | AC8 |
| X9 | An operation of another service is written into this document as provided | The review fails: the document lists only rwb-reporting's own operation | None | AC1 |
| X10 | The document declares an event type of this view | The review fails: the capability publishes only the local record of DP-03 | None | AC8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the two same-service contracts it extends and the Ownership Map only |
| Negotiable | Property names and lengths are settled with the consumers; the operation, the variance rule, the period rule and the order are fixed by the target architecture |
| Valuable | Unblocks the app story of this legacy key on Day 1 and every consumer of the measure answer, the dashboard and the audit sample |
| Estimable | One document, one additive change, one consumed element, nine contract tables and three fakes |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the benefit-realisation view

  Background:
    Given the service naming rule of the platform library is in force
    Given the rwb-reporting read surface is published under the base /api/recovery/reporting/v1
    Given the ownership map gives GET /reports/measures to rwb-reporting

  Scenario: AC1 The read operation is declared with its owner and the change is additive (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-reporting is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares GET /reports/measures under the base /api/recovery/reporting/v1 and owned by rwb-reporting
    Then the document names no other service's operation as provided
    Then every added property is optional in the schema, so a consumer of the previous version of the answer keeps working
    Then it declares the response header X-Data-As-Of

  Scenario: AC2 The period and the baseline date are parameters of the answer (new, D-RCV-60)
    Given the GET /reports/measures operation declared in the document
    When its parameters are reviewed
    Then the request takes measure, product, route, from, to and baselineDate
    Then from and to name the first and the last day of the period asked for, and a period whose from is after its to is refused with 422 and MSG-GEN-003
    Then baselineDate names the frozen baseline the values are compared with and defaults to the baseline of the definition version in force, 2026-11-27 for "MD-2026.11" (GAP-2580; ASM-4259)
    Then an empty required parameter is refused with 422 and MSG-GEN-001

  Scenario: AC3 The measure row fixes the value and its comparison (new, D-RCV-60)
    Given the row component of GET /reports/measures declared in the document
    When its properties are reviewed
    Then each row carries measureCode, definitionVersion, period, productGroup, dimensionCode, dimensionValue, unit, value, baselineValue, variance, variancePercent, isBaseline, frozen and staleDate
    Then the document states that value is the measure of the period, baselineValue is the frozen value of the same measure, product and dimension, and isBaseline and frozen are read from measure_snapshot and never recomputed by a consumer
    Then the document states that the rows are ordered by measureCode, then productGroup, then dimensionCode, and that the answer is one bounded array with no paging in major version 1 (GAP-2580; ASM-4257)
    Then the units are the rows of LOV-MEASURE-UNIT and the dimensions the rows of LOV-MEASURE-DIM, never values written in the document

  Scenario: AC4 The variance rule is part of the contract (new, D-RCV-60)
    Given the variance properties of AC3
    When the rule of their computation is reviewed
    Then variance is value less baselineValue and variancePercent is variance over baselineValue, written only when baselineValue is not zero (GAP-2580; ASM-4256)
    Then a measure with no frozen baseline row answers baselineValue null, variance null and variancePercent null with no error
    Then the document states that no consumer computes, rounds or re-bases a variance, and that the baseline rows are never rewritten

  Scenario: AC5 The error envelope and the message codes (new, D-RCV-60)
    Given the error responses declared on the operation
    When each condition is mapped to its status and its message ID
    Then 401 no session, 403 a missing right, 422 an inverted period or an empty required parameter, and 503 a store failure are declared with the platform envelope
    Then 422 an inverted period maps to MSG-GEN-003 and an empty required parameter to MSG-GEN-001, 403 to MSG-P4-002 and 503 to MSG-P7-003
    Then MSG-P1-001 is declared as the stale flag of a measure and not as an error
    Then every text is the legacy text of RWB-E6-037 unchanged and the envelope is the platform envelope, never a local one

  Scenario: AC6 The right and the scope the answer requires (new, D-RCV-60)
    Given the security and scope statements of the operation
    When they are compared with the roles and the right names of the target
    Then GET /reports/measures requires Reporting, right R, with the scope applied
    Then the scope filters every row before any value, count or percentage is computed, so a value never includes a case the caller may not read
    Then RW-FINANCE holds Reporting R, and a role without the right is refused with 403 and MSG-P4-002 and never with an empty answer
    Then the contract declares the right and the scope only: the guard that applies them belongs to the platform library and is not redefined here

  Scenario: AC7 The freshness stamp and the stale flag (new, D-RCV-60)
    Given the header and the stale property of AC1 and AC3
    When the stale rule is reviewed
    Then X-Data-As-Of carries the business date of the answer and is omitted when that date is not known inside the budget
    Then staleDate carries the last complete data-product date of a measure whose source has not arrived, and it is null when the source is complete
    Then the document states that a stale measure keeps its value and its date and is never silently dropped or recomputed from an older month

  Scenario: AC8 The consumed element, the one write of the capability and the 2 s budget (new, D-RCV-60)
    Given the consumed and published elements of the document
    When they are compared with the Ownership Map and the platform
    Then the readiness answer of the data products names P1 rwb-source-data as its owner, is declared as an activity on the owner's queue with a 2 s budget and is faked (DP-05)
    Then the local decision record of a tracked month is declared as the one write of the capability, written by the library of DP-03 and relayed on rwb.decision-record.v1
    Then the document publishes no event type of its own on rwb.reporting.events.v1 and subscribes to none (GAP-2580; ASM-4258)
    Then no REST operation of another service is declared as consumed and no Temporal Schedule is registered

  Scenario: AC9 The nine contract tables are complete and the fakes match them (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map or None where the element is empty
    Then 12.3 and 12.4 record None and name the local record and the events that move the facts as published by their own stories
    Then 12.6 records None and names JOB-15 as the Schedule of RWB-P9-E2009-APP
    Then the three contract fakes answer the path and the payload of 12.1, the shape of the consumed readiness answer and the merged screen section, and the contract tests compare each fake with the document and fail on any drift
```

These nine criteria are new for the contract baseline and test the artefact only; they restate no business outcome owned by RWB-P9-E6037-APP, which keeps the two legacy criteria with their own tags.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/reporting/v1`; the document never declares another service's path as provided | DP-13; Template and Rules §R4 |
| BR2 | Event names are `rwb.<short>.<Event>.v1` on the topic `rwb.<short>.events.v1`, with retry and `.dlt` topics, and this view carries no event type | DP-14; Template and Rules §R4 |
| BR3 | A read declares no Idempotency-Key and writes nothing; a command declares it and stores its response | ADR-020; DP-09 |
| BR4 | Error responses use one envelope and one message ID per condition; the business texts are copied unchanged from the legacy story | Template and Rules §R7.2 s14 |
| BR5 | A schema change is additive within a major version; a breaking change is a new major version | Template and Rules §R7.2 s12 |
| BR6 | The document lists only operations owned by rwb-reporting; a consumed element is described as consumed and faked, never as provided | Ownership Map v1 |
| BR7 | The variance is computed by the owner and declared in the contract, so no consumer can compute a second version of the same number | Legacy AC1; GAP-2580; ASM-4256 |
| BR8 | The baseline is the frozen baseline of the definition version in force and is never rewritten, re-based or recomputed | RWB-E1-013 baseline of 2026-11-27 |
| BR9 | No business value is fixed in the contract: measure codes, formulas, units, dimensions and the publish state stay data rows | Principle 1; FSD P9 BR-P9-006 |
| BR10 | No personal data is declared in an answer: rows carry measure codes, codes, counts, amounts, days, percentages, dates and a definition version only | DP-19; TSD P9 T6.2 |
| BR11 | The order and the period of the answer are part of the contract: a consumer that sorts or re-bases differently from the document has a defect | TSD P9 T-A.2 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The operation, the variance rule, the period rule and the order are described | In review |
| In review | Consumer sign-off | The app story, the dashboard and the audit consumers accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example a new dimension | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or the variance rule changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | An event type of the view appears in the document | The review of AC8 fails | In review |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-reporting | Owns the OpenAPI document and the fakes of the operation; tags the baseline |
| Solution architect | Approves a breaking change and a new major version |
| Consuming teams (the app story, the dashboard, the extract hand-over and the audit sample) | Review and sign off the parts they consume |
| rwb-source-data owner | Signs off the readiness row, its budget and the stale rule |
| Platform library owner | Owns the error envelope, the naming rule and the guard this document reuses |
| Data steward | Confirms that no personal data field is declared in the answer |

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Measure row | `measureCode`, `definitionVersion`, `period`, `productGroup`, `dimensionCode`, `dimensionValue`, `unit`, `value`, `baselineValue`, `variance`, `variancePercent`, `isBaseline`, `frozen`, `staleDate` from `measure_snapshot` DF-RPT-042 to DF-RPT-051 and `measure_definition` DF-RPT-032, DF-RPT-036 and DF-RPT-037 |
| Period | `from` and `to` naming the first and last day; `period` in the row is the month the rows belong to (GAP-2580; ASM-4259) |
| Baseline | `baselineDate` and the frozen rows of 2026-11-27 read beside the period; never rewritten |
| Variance | `variance` and `variancePercent`, computed by the owner (GAP-2580; ASM-4256) |
| Lists | LOV-MEASURE-UNIT COUNT, THB, DAYS, PERCENT; LOV-MEASURE-DIM ROUTE, AGE_BAND, QUEUE, STAGE, AGENT; LOV-PRODUCT MORTGAGE, HIRE_PURCHASE, SSME, UNSECURED; LOV-DATA-PRODUCT DP01 to DP14, from TSD P9 T3.2 |
| Freshness | The `X-Data-As-Of` header and `staleDate`, from the readiness answer of rwb-source-data |
| Error envelope | The platform envelope with one message ID per condition; the texts of section 14 |

The field-level types, lengths and required flags of the added properties are settled in the baseline review; this story fixes the names, the optionality rule of AC1, the variance rule of AC4, the period rule of AC2 and the order of AC3.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-reporting (P9); base `/api/recovery/reporting/v1`.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| GET | `/reports/measures` | Measure array: filters `measure`, `product`, `route`, `from`, `to`, `baselineDate`; rows with `measureCode`, `definitionVersion`, `period`, `productGroup`, `dimensionCode`, `dimensionValue`, `unit`, `value`, `baselineValue`, `variance`, `variancePercent`, `isBaseline`, `frozen`, `staleDate`; header `X-Data-As-Of` | Reporting R, scope applied |

The operation answers 401, 403, 422 and 503; it takes no Idempotency-Key and writes nothing. The answer is one bounded array with no paging in major version 1, ordered by `measureCode`, then `productGroup`, then `dimensionCode`. `baselineDate` defaults to the baseline of the definition version in force, and a baseline date with no frozen row answers null variance and is never an error.

#### 12.2 REST operations consumed

None. The data-product readiness of the month is consumed as an activity on the queue of P1 rwb-source-data, and the local decision record is written through the library of RWB-PLT-E1027-CON; neither is a REST operation of another service, so no hop and no breaker is declared here.

#### 12.3 Events published

None. The contract publishes no event type. `rwb.reporting.events.v1` exists with its `.retry` and `.dlt` topics, and the publish marker of a measure run belongs to the Epic 1 measure story; this view publishes nothing of it (GAP-2580; ASM-4258). The one write of the capability — the local decision record of a tracked month — is relayed on `rwb.decision-record.v1` by the library of DP-03 and is declared as consumed, not as published here.

#### 12.4 Events consumed

None as a subscription of this contract. The facts of a month are replayed by the run of RWB-P9-E6037-APP from the events of P3, S2, S6, S7, P6 and P2 and from `DecisionRecorded` on `rwb.decision-record.v1`; their types are owned and published by those services, and this document declares their consumer groups once so that the owner of each type can see who reads it. The read path of this contract subscribes to nothing.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `reportingMeasuresDaily` (JOB-15, owned by RWB-P9-E2009-APP) | Workflow, one execution per business date | `rwb-reporting` | Carries the month step whose rows this contract publishes; owned by the measure story, named here as the writer |
| The data-product readiness of a month | Activity, on the owner's queue | `rwb-source-data` | The consumed element of 12.2 and AC8; faked |

No workflow, activity or child workflow is registered by this story; the rows fix what a consumer of the answer may assume about the writer.

#### 12.6 Schedules

None. The 01:30 daily Schedule `reportingMeasuresDaily` (JOB-15) is RWB-P9-E2009-APP's; this baseline registers no Schedule, no cron entry and no job name, and the monthly view is a period of the same rows rather than a second job.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `measure_definition` | P9 (`rwb_reporting`) | The definition version, the formula, the data product and the unit behind every row |
| `measure_snapshot` | P9 (`rwb_reporting`) | The value, the baseline flag and the frozen flag of a measure, business date, product and dimension |
| `decision_record` | PLT library, created in `rwb_reporting` | The record of a tracked month that a consumer may cite; written by the library, never by the read path |
| `outbox_event`, `processed_event` | PLT library, created in `rwb_reporting` | The envelope of the record and the inbox of the replayed events; not written by the read path |

Never read as a table: `recovery_case` and `queue` (P3), the treatment record (S2), the notice record (P6), the write-off and debt-sale records (S7, S6), `decision_log_entry` (P7) and every `v_ace_*` view. No foreign key leaves the schema (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-reporting OpenAPI fake | `GET /reports/measures` for 2026-12-01 to 2026-12-31 with the six measures beside the baseline of 2026-11-27, `X-Data-As-Of` 2026-12-31, a measure with null variance, an inverted period and a refusal without Reporting R | App story, dashboard, audit sample, contract tests |
| rwb-source-data readiness fake | Every source complete to 2026-12-31, one source stale to 2026-12-14, and a delayed answer beyond 2 s | App story, contract tests |
| Decision-record library stub | A healthy chain returning the sequence and the entry hash, and a stopped chain returning MSG-P7-003 | App story, contract tests |
| gateway-bff composite route fake | The merged SCR-37 answer with the benefit section, the period selector and the stale flag | Dashboard consumers, contract tests |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 0 consumed | `/reports/measures` on `/api/recovery/reporting/v1`; no cross-service REST call |
| Kafka | None published, none consumed by the read path | The month's events are replayed by the run and are owned by P3, S2, S6, S7, P6 and P2; the local record is relayed on `rwb.decision-record.v1` by the library |
| Temporal | None registered | The writer is `reportingMeasuresDaily`, owned by RWB-P9-E2009-APP |
| File | None | No file in this contract |

### 13. Solution plan

**Deliverables.** The additive change to `openapi/rwb-reporting-v1.yaml` for `GET /reports/measures`, the `Measure` row component shared with RWB-P9-E2009-CON and RWB-P9-E1013-CON, the contract README rows for the variance rule, the period rule, the order and the stale rule, and the four WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`: the record of a tracked month is declared as the one write of the capability | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | The data products of a month are read through rwb-source-data's readiness and snapshot answer; this document declares no view and no cross-schema join | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/reporting/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route for SCR-37 | H RWB-PLT-N001-CON |

No pattern is claimed outside this list: the baseline registers no Schedule, so DP-10 is not applied, and the answer carries no personal data, so no masking pattern is added.

**Build steps**

1. Add the `baselineDate` parameter, the four row properties and the stale flag to the document; validate the additive rule of AC1 in the pipeline.
2. Write the variance rule of AC4 and the period rule of AC2 into the document and the README, so a consumer cannot compute a second version of a benefit number.
3. Fix the order and the absence of paging of AC3, with the platform parameter as the only ceiling.
4. Record the consumed readiness row and the one write of the capability; state the absence of events of AC8.
5. Map every failure code of AC5 and compare each text with the legacy text.
6. Publish the four fakes and the nine contract tests; a drift between a fake and the document fails the build.
7. Baseline tag and the consumer sign-off note, including the rwb-source-data owner and the consumers of the answer.

**Done when.** The OpenAPI artefact validates in the pipeline, the nine contract tests pass, the four fakes answer every path and the drift test is green, and RWB-P9-E6037-APP and the consumers of the answer have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required parameter is empty | Enter {field}. |
| MSG-GEN-003 | `from` is after `to` | {field} cannot be before {other}. |
| MSG-P4-002 | The role lacks the Reporting right | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The record of a month cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | A source of the period is stale | {product} is from {date}. Today's ACE batch has not arrived. |

The message IDs are contract elements and the texts are the agreed legacy and FSD P9 texts unchanged. Which data product fills the `{product}` of MSG-P1-001 for a given measure is Not specified in the source documents (GAP-2580; ASM-4258); the row of `measure_definition` names it.

### 15. Screens and states

The contract serves the benefit section of SCR-37 Steering dashboard (capability area Reporting) through the gateway-bff composite route (DP-19), in the states Loading, Published month, Stale, No baseline and Error. The legacy story says "No screen in this story"; the section is the read surface the FSD A2.6 gives the Finance and CFO delegate, and its screen field order, masking and merge order belong to RWB-PLT-N001-CON. The contract fixes the rwb-reporting answer only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P9-E6037-CON-01 | AC1 | Contract | The document validates; the operation, its owner, the header and the optional properties are present |
| TC-P9-E6037-CON-02 | AC2 | Contract | The six parameters; first and last day; an inverted period refused with MSG-GEN-003; `baselineDate` default 2026-11-27 |
| TC-P9-E6037-CON-03 | AC3 | Contract | The fourteen row properties; the order by measure, product and dimension; the bounded array |
| TC-P9-E6037-CON-04 | AC4 | Contract | Variance 562,000.00 and 12.92 percent on a baseline of 4,350,000.00; a row with null variance; a zero baseline |
| TC-P9-E6037-CON-05 | AC5 | Contract | Every condition mapped to its status and message ID; the five texts compared with the legacy and FSD texts |
| TC-P9-E6037-CON-06 | AC6 | Contract | Reporting R; the scope filter before the value; the 403 shape for a role without the right |
| TC-P9-E6037-CON-07 | AC7 | Contract | `X-Data-As-Of` present and omitted; `staleDate` set and null |
| TC-P9-E6037-CON-08 | AC8 | Contract | The readiness row with its owner and budget; the record as the one write; no event type; no Schedule |
| TC-P9-E6037-CON-09 | AC9 | Component | The nine sub-tables present with owners; four fakes match the document; a drifted fake fails the build |

The nine criteria are tested against the artefact, not against a business outcome. The four legacy test cases of RWB-E6-037 are owned and tested by RWB-P9-E6037-APP and are not copied here; `-ITG` copies belong to the wave 4 integration harness.

### 17. Guardrails

- No business value in the contract: measure codes, formulas, units, dimensions and the definition version are data rows, and the baseline date is a parameter, never a constant.
- No personal data in a schema, an example or a fake: measure codes, codes, counts, amounts, days, percentages, dates and a definition version only.
- The contract names only rwb-reporting's tables and only the operation owned by rwb-reporting; the readiness element is consumed and faked, never declared as provided (DP-01, DP-05).
- One REST base and one topic per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The variance is computed once, by the owner; a consumer that re-bases or re-rounds it has a defect, not a preference.
- No retired element is reintroduced: a build that declares a data-lake target, a second extract or a benefit Schedule fails the absence test of AC9 (DP-17).
- Every example in the document is synthetic; no production payload is copied into a schema or a fake.
- The error envelope, the guard and the naming rule come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| None (the legacy story carries no requirement ID) (GAP-2580; ASM-4258) | Track the measures in the benefit model against the baseline, monthly | The operation, the period and the baseline parameters, the row and the variance rule | TC-P9-E6037-CON-01, TC-P9-E6037-CON-03, TC-P9-E6037-CON-04 |
| NFR-065 | Business measures per decision are produced from the decision log and not from a separate count | The rows and the definition version a value is produced under | TC-P9-E6037-CON-03 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The operation and its error envelope; the readiness element and its budget | TC-P9-E6037-CON-05, TC-P9-E6037-CON-08 |
| DP-03 | The decision is recorded locally and published on `rwb.decision-record.v1` | The record of a tracked month as the one write of the capability | TC-P9-E6037-CON-08 |
| DP-05 | ACE data is reached only through the owner's contract | The readiness row and the declaration that no view is read | TC-P9-E6037-CON-08 |

The legacy endpoint of RWB-E6-037 moves to the per-service base and keeps its operation path (DP-13); the legacy `v_ace_score` read is replaced by the events of the run and by the readiness answer, and no view of this service is declared.

### 19. Out of scope

- The behaviour of the answer: the month step, the calculators, the month rows and the read implementation (RWB-P9-E6037-APP).
- The baseline measure set and the shapes of `measure_definition` and `measure_snapshot` (RWB-P9-E1013-CON and RWB-P9-E1013-APP).
- The base `Measure` resource, the steering measures and the daily publish or hold (RWB-P9-E2009-CON and RWB-P9-E2009-APP).
- The deployment, the consumer groups, the dashboards and the runbook of this capability (RWB-P9-E2009-OPS).
- The decision record of a tracked month as a library behaviour: consumed and faked, never defined here (RWB-PLT-E1027-CON).
- The readiness answer of rwb-source-data as a contract: consumed and faked, never defined here.
- The gateway-bff composite route and the screen field list (RWB-PLT-N001-CON).
- The cross-service journey harness and its evidence, when a wave 4 journey story is raised for this legacy key.

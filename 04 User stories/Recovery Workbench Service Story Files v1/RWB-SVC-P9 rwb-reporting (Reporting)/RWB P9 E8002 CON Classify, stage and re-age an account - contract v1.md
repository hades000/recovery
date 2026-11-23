# RWB-P9-E8002-CON Classify, stage and re-age an account — contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P9-E8002-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-reporting |
| Service epic | RWB-SVC-P9 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-E8-002 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P9 rwb-reporting v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

| Version | Date | Change | Tool |
|---|---|---|---|
| v1 | 22 November 2026 | D-RCV-60 realignment of RWB-E8-002 into rwb-reporting, contract slice | T3 Code / OpenCode / DeepSeek v4.1 Flash |

### 1. Story

As a **tech lead**, I want **the published contract baseline of the classification, staging and re-ageing capability of rwb-reporting — the single provided measure read with the documented meaning of its STAGE, AGE_BAND and ROUTE dimension values, the rule-version read of rwb-decision, the four subscriptions with their consumer groups and envelope rules, the change record on `rwb.decision-record.v1`, the negative declarations of the new table, the new column, the event and the file, the four owned tables as shapes, the message map and the five fakes**, so that **the app story of this legacy key builds against one fixed, testable contract on Day 1 and a segment can never be reported without the rule version that produced it**.

What the baseline fixes, and nothing else:

- the one provided operation of the service — `GET /reports/measures` (API-P9-001) — on base `/api/recovery/reporting/v1`, with its filters, its access right, its freshness header and the documented meaning of the three dimension values it returns (DP-13);
- the negative shape statement: the reported classification adds no table and no column, because it rides `measure_snapshot.dimension_code` and `dimension_value` as they stand (GAP-2585; ASM-4278);
- the rule-version read of rwb-decision as a consumed declaration with a fake, with no C row in the plan (GAP-2585; ASM-4277);
- the four subscriptions of the capability with their consumer groups and their envelope rule, and no published event of the service's own;
- the change record on the shared `rwb.decision-record.v1`: FEAT-RPT-10 as the decision reference, the rule id, the rule version, the from stage, the to stage, the age band and the business date (DP-03);
- the message map and the error model, so a consumer and the screen read one envelope.

This story writes no behaviour: the step, the projection and the rows are RWB-P9-E8002-APP. Where no published document fixes an element, the baseline states the placeholder and the gap, and no business value is invented.

### 2. Business rationale

Contract-first REST with one hop is the decoupling decision (DP-13, ADR-020), and the ownership row of the service gives it exactly one provided operation and three tables. The baseline therefore fixes that one operation and nothing else: no second path is invented for a classification, because the classification is not a resource of its own — it is the dimension semantics of the measure rows the service already returns.

The sharper part of the baseline is what it says in the negative. A classification contract is the easiest place in the system to freeze a band, a threshold or a stage code into a schema, and that would contradict BR-P9-010 and the principle that no value a business person may change is written in code. So the baseline fixes shapes, references and the version stamp, and states once that the stage set, the age bands and their thresholds are rule rows of the version in force and never members of an answer. The same rule shapes the record element: it carries the rule id and the rule version, and no stage list of its own.

The contested points are carried as gaps and assumptions rather than settled quietly: the rule read of rwb-decision has no published member names and no C row in the plan, the upstream reclassification event has no name in the sources, the decision reference of the record is not fixed by the legacy story, and the legacy story puts the recompute in module P9 while rule R-UNI-22 puts the same recompute on the Workbench (GAP-2585, GAP-2586; ASM-4277, ASM-4281).

### 3. Preconditions

- The service template and the naming library are in force, so the base, the schema, the topic and the queue follow the platform rule and not a local choice (RWB-PLT-TPL).
- The platform error envelope, the CloudEvents 1.0 envelope and the retry and `.dlt` topic convention are the platform baseline (RWB-PLT-EVT, RWB-PLT-TE006-CON); this document narrows them and never redefines them.
- The decision-record library of DP-03 and the shared topic `rwb.decision-record.v1` are available as a platform contract (RWB-PLT-E1027-CON).
- The gateway-bff composite route contract is available, so the read of the baseline is reached the way the screen reaches it (RWB-PLT-N001-CON, DP-19).
- The operations, tables and events of section 12 are taken from the ownership rows of the context pack and the Ownership Map only: `measure_definition`, `measure_snapshot` and `measure_publish` are rwb-reporting's, JOB-15 is its one job, and it owns no event and no workflow.
- The parent baselines of the service — RWB-P9-E1013-CON for the measure set and the `Measure` shape, RWB-P9-E2009-CON for the publish row and the steering delta — are readable, so this baseline publishes only the increment of this key and does not restate them.
- No build dependency: a CON story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Read the ownership rows and the parent baselines, and list the one operation, the three owned tables with the library's record, the four subscriptions and the one job of this key.
2. Document the one provided read, `GET /reports/measures` (API-P9-001), on the per-service base, with its five query parameters, its 200 answer, its five error responses and its right.
3. Document the meaning of the STAGE, AGE_BAND and ROUTE dimension values of the answer: the re-aged classification of the row's business date under the rule version in force, with the version carried by the row's `definition_version` and by the record.
4. State the negative shape rule: no new table, no new column, no new member for a band, a threshold or a stage code.
5. Declare the rule-version read of rwb-decision as consumed, one hop, faked, with no C row, and record the placeholder for the member names no published document fixes.
6. Declare the four subscriptions with their topic, their consumer group and their envelope rule, and state once that the service publishes no event of its own.
7. Fix the change record element: FEAT-RPT-10 as the decision reference, the rule id, the rule version, the from and to stage, the age band, the business date and the applied date, on the shared topic through the library.
8. Fix the message map of section 14 and the status of each message, so a refusal, a missing version and a stopped record answer one envelope.
9. Publish the five fakes, the seven contract tests, the tag `v1` and the sign-off note to RWB-P9-E8002-APP.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the envelope | The platform schema message | AC1 |
| X2 | A member is added or renamed within major version 1 | The contract test fails; a removal, a rename or a retype needs a new major version | None | AC7 |
| X3 | The document freezes a stage code, an age band or a threshold as a member or an example value | The closed-set test fails the build | None | AC2 |
| X4 | The declaration adds a table or a column for the classification | The negative-shape test fails the build | None | AC3 |
| X5 | A subscription is declared without a consumer group or an envelope rule | The declaration is not publishable and the tag is refused | None | AC4 |
| X6 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X7 | The document declares another service's operation as provided, or restates a parent baseline | The review fails the baseline; the element is described as consumed and faked | None | AC5 |
| X8 | An element of the classification has no published document behind it and its owner has not confirmed the names | The declaration carries the placeholder and the fake answers the baseline shape; the review row stays open | None | AC5, GAP-2585 |

X8 is the only path that ends in an open review row; the rest are gates of the tag. No path invents a business value: the stages, bands and thresholds are rule rows of the version in force.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the ownership rows, the parent baselines and the naming rule only |
| Negotiable | The member names of the rule read, the decision reference of the record and the dimension description are settled with the rwb-decision, gateway-bff and reporting owners; the base, the topic and the subscription rule are fixed by the target |
| Valuable | Unblocks the app story on Day 1 and stops a band, a threshold or a stage code from ever becoming a contract constant |
| Estimable | One document increment, one consumed declaration, four subscriptions, one record element, nine contract tables, five fakes and seven contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact and not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the classification, staging and re-ageing of rwb-reporting

  Background:
    Given the service naming rule of the platform library is in force
    Given the base of rwb-reporting is /api/recovery/reporting/v1 and its schema is rwb_reporting
    Given the ownership rows give rwb-reporting one provided operation, three tables, no event, one job and no workflow

  Scenario: AC1 The one provided read is declared and validates (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-reporting is published with the increment of this key
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares GET /reports/measures under the base /api/recovery/reporting/v1, owned by rwb-reporting, with the query parameters measure, product, route, from and to
    Then the operation declares capability area Reporting with right R and scope applied
    Then it declares the responses 200, 400, 401, 403, 422 and 503 with one envelope and one message ID per condition
    Then it declares no other path as provided, and API-P9-001 stays the only row of the service

  Scenario: AC2 The dimension values of the read are documented and freeze no business value (new, D-RCV-60)
    Given the documented meaning of the STAGE, AGE_BAND and ROUTE dimension values of the answer
    When the description and the examples are compared with the rule source
    Then each value is described as the re-aged classification of the row's business date under the rule version in force
    Then the row carries its definition_version and its businessDate beside the value
    Then no stage code, age band, threshold, route code or measure code appears as a member, a default or an example value
    Then a build that freezes one of them as a member or an example fails the closed-set test

  Scenario: AC3 The classification adds no table and no column (new, D-RCV-60)
    Given the shape statement of the baseline
    When it is compared with TSD P9 T3.1 and the ownership rows
    Then the reported classification rides measure_snapshot.dimension_code and dimension_value as they stand
    Then the baseline declares no new table, no new column, no view and no index beyond the one of the app story
    Then no foreign key and no statement leaves rwb_reporting
    Then a declaration that adds a table or a column for the classification fails the negative-shape test

  Scenario: AC4 The four subscriptions are declared with their groups and their envelope rule (new, D-RCV-60)
    Given the event section of the baseline
    When it is compared with the event catalogue and the connection matrix
    Then rwb.case.CaseCreated.v1 and rwb.case.CaseStateChanged.v1 are declared as consumed on rwb.case.events.v1, owner P3, keyed by caseId
    Then rwb.decision.RulePackageInForce.v1 is declared as consumed on rwb.decision.events.v1, owner P7
    Then the upstream reclassification fact is declared with its owner and its topic named only, and its event name is Not specified in the source documents (GAP-2585; ASM-4277)
    Then each row names a consumer group and the dedupe rule by the CloudEvents id through the inbox
    Then the baseline declares no published event of the service and no second topic for this capability

  Scenario: AC5 The rule-version read and the change record are declared, and no other service's operation is provided (new, D-RCV-60)
    Given the consumed declarations and the record element of the baseline
    When they are reviewed against the parent baselines and the decision library
    Then the rule rows and the rule version in force are declared as consumed from rwb-decision on its base, one hop, with a fake and with no C row in the plan
    Then the member names of that read carry the placeholder where no published document fixes them
    Then the change record is declared on the shared rwb.decision-record.v1 through the library with the decision reference FEAT-RPT-10, the rule id, the rule version, the from and to stage, the age band and the business date
    Then the record fixes no stage list, no band and no threshold
    Then no element of a parent baseline is restated in this document

  Scenario: AC6 The five fakes reproduce their documented answers (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the operation, the declaration or the subscription it serves
    Then the rule read fake answers one version in force and a date with no version
    Then the event harness answers one account opening, one stage change and one rule version reaching its valid-from date
    Then the record stub answers an accepted record with the rule id and the rule version and a stopped chain
    Then the measure read fake answers the re-aged dimension values with X-Data-As-Of, and the route fake the merged screen answer
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 A breaking change opens a new version and the tag stays buildable (new, D-RCV-60)
    Given the baseline is tagged v1
    When a consumer proposes a removal, a rename or a retype of a published member
    Then the change is published as v2 with its own document and fakes
    Then the tag v1 stays readable and RWB-P9-E8002-APP still builds against it
    Then the change is recorded in the Change Register
```

The seven criteria test the baseline only and carry no stage code, no age band, no threshold and no measure value; the three legacy criteria AC1 and AC2 of RWB-E8-002 stay with RWB-P9-E8002-APP and none of them is copied here.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/reporting/v1`; the document never declares another service's path as provided | DP-13; Template and Rules §R4 |
| BR2 | The topic is `rwb.reporting.events.v1` and an event would be `rwb.reporting.<Event>.v1`; this service owns no event of this key | DP-14; ownership rows |
| BR3 | Every consumed event carries the CloudEvents 1.0 envelope, is keyed by caseId and carries no personal data | Architecture v5 event notes |
| BR4 | The change record is the library's entry on the shared `rwb.decision-record.v1`, never an event of this service | DP-03 |
| BR5 | No value a business person may change is a contract constant: stages, routes, age bands, thresholds and measure codes are rule rows or definition rows of their owners | BR-P9-010 |
| BR6 | The classification adds no table and no column; it rides the existing dimension columns of `measure_snapshot` | DF-RPT-046, DF-RPT-047 (GAP-2585; ASM-4278) |
| BR7 | A read declares no Idempotency-Key and no request body; this baseline has no POST of its own | Platform baseline |
| BR8 | Error responses use one envelope and one message ID per condition; the legacy texts stay unchanged | Template and Rules §R7.2 s14 |
| BR9 | A shape change is additive within major version 1; a breaking change is a new major version | Architecture v5 API notes |
| BR10 | The document lists only operations, tables and jobs owned by rwb-reporting | Ownership Map |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The operation, the dimension meaning, the negatives, the subscriptions and the record element are described | In review |
| In review | Consumer sign-off | The app story and the rwb-decision, gateway-bff and platform owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A member is added within major version 1 | Baselined |
| Baselined | Breaking change | A member is removed, renamed or retyped | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A band, a threshold or a stage code appears as a member or an example | The closed-set test of AC2 fails | In review |

The row and publish states of the app story are the app story's; this baseline fixes shapes and moves nothing.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-reporting | Owns the document and the fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version and any correction of the ownership rows the baseline consumes |
| Owner of rwb-decision (P7) | Confirms or corrects the rule-version declaration and its fake |
| Owner of rwb-case (P3) | Confirms the two case subscriptions and their envelope rule |
| Owner of rwb-source-data (P1) | Confirms the upstream reclassification declaration and its topic |
| Platform library owner | Owns the CloudEvents envelope, the error envelope, the naming rule and the decision library |
| Data steward | Confirms that no personal data field and no band appears in the answer, the record or a fixture |

The per-service login name behind the security scheme is not part of this baseline; the document names the scheme "the rwb-reporting login (DP-02)".

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Measure answer | `measureCode` DF-RPT-032, `name` DF-RPT-033, `definitionVersion` DF-RPT-037, `businessDate` DF-RPT-044, `productGroup` DF-RPT-045, `dimensionCode` DF-RPT-046, `dimensionValue` DF-RPT-047, `value` DF-RPT-048, `caseCount` DF-RPT-049, `unit` DF-RPT-036 |
| Dimension values | STAGE, AGE_BAND and ROUTE of LOV-MEASURE-DIM, as the re-aged classification of the row's business date |
| Change record | FEAT-RPT-10 as the decision reference, the rule id, the rule version, the from and to stage, the age band, the business date and the applied date; DF-DEC-001 to DF-DEC-018 |
| Consumed facts | the case id, the product group, the stage, the route and the entry date of a case; the rule id, the rule version and the valid-from date of a rule set; codes, dates and counts only |
| Not declared | any band, threshold, stage list, route list, measure code or personal field; any new table or column (GAP-2585; ASM-4278) |

The member names of the rule read and the decision reference of the record are Not specified in the source documents (GAP-2585; ASM-4277); this baseline fixes the element names above and leaves the rest to the baseline review.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-reporting (P9); base `/api/recovery/reporting/v1`.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/reports/measures` | Measure[] of status 200: the members of section 11, filtered by measure, product, route, from and to, with the header `X-Data-As-Of` | Reporting, right R, scope applied | Not applicable |

The operation answers 400, 401, 403, 422 and 503 with the error envelope and one message ID of section 14. It is the only provided operation of the service and this baseline adds no path, no parameter and no member beyond the parent documents.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| GET | the rule-version read of `/api/recovery/decision/v1` | P7 rwb-decision | the rule id, the rule version, the valid-from date, the stage set and the age bands of a business date, faked; the member names carry the placeholder (GAP-2585; ASM-4277) |

One row, one hop, on the owner's published contract; the plan declares no C row for it and the document declares no other consumed operation.

#### 12.3 Events published

None. The shared `rwb.decision-record.v1` carries the change record of section 11 through the local library of DP-03, and the ownership rows give the service no event of its own on `rwb.reporting.events.v1`.

#### 12.4 Events consumed

| Event | Topic | Consumer group | Envelope rule | Declared element |
|---|---|---|---|---|
| `rwb.case.CaseCreated.v1` (EV-01) | `rwb.case.events.v1` | `rwb-reporting.case.v1` | dedupe on the event id; order per case by the outbox sequence | caseId, productGroup, accounts, businessDate |
| `rwb.case.CaseStateChanged.v1` (EV-05) | `rwb.case.events.v1` | `rwb-reporting.case.v1` | as above | caseId, fromState, toState, ruleId, decisionLogEntryId |
| `rwb.decision.RulePackageInForce.v1` (EV-30) | `rwb.decision.events.v1` | `rwb-reporting.decision.v1` | dedupe on the version id | packageCode, packageVersion, versionId, validFrom, approvedBy |
| The upstream reclassification and re-age fact (name Not specified in the source documents (GAP-2585; ASM-4277)) | the owner's topic, named by the catalogue | `rwb-reporting.classification.v1` | dedupe on the event id and the account reference | the account reference, the classification and the re-age date |

The connection matrix names rwb-reporting as a listener of P3, S2, S3, S5, S6, S7 and P6, and the shared `rwb.decision-record.v1` carries the decision records of P7; the four rows are the ones this capability needs and none of them is a new claim about who publishes.

#### 12.5 Workflows and activities

None. The ownership rows give rwb-reporting no workflow; the step runs inside JOB-15 of section 12.6 and inside the service's own event handler, and the baseline declares no child workflow, no activity contract and no Nexus call.

#### 12.6 Schedules

| Job | Queue | When | Contract element |
|---|---|---|---|
| JOB-15, the daily reporting run of rwb-reporting | `rwb-reporting` | Daily at 01:30 | the classification step of the app story; the baseline declares no second Schedule and no Quartz row |

#### 12.7 Tables owned

| Table | Schema | Contracted use | Key |
|---|---|---|---|
| `measure_snapshot` | `rwb_reporting` | the STAGE, AGE_BAND and ROUTE dimension rows of a business date | unique on (measure_code, definition_version, business_date, product_group, dimension_code, dimension_value) |
| `measure_definition` | `rwb_reporting` | the definition in force of the measures that carry the three dimensions | inherited from RWB-P9-E1013-CON |
| `measure_publish` | `rwb_reporting` | the PUBLISHED or HELD status of the business date | inherited from RWB-P9-E2009-CON |
| `decision_record` | PLT library, created in `rwb_reporting` | one local record per changed account | hash chain per record kind |

No new table and no new column is declared (BR6). `recovery_case`, `decision_log_entry` and `rule_row` are other owners' tables and are named only as consumed answers.

#### 12.8 Contract fakes

| Fake | Documented answer | Consumers |
|---|---|---|
| Rule read fake (rwb-decision) | one classification rule version in force with its stage set and age bands; a business date with no version in force | APP, contract tests |
| Event harness | one account opening, one stage change and one rule version reaching its valid-from date | APP, contract tests |
| Decision-record stub | an accepted record with the rule id and the rule version; a stopped chain returning MSG-P7-003 | APP, contract tests |
| Measure read fake (rwb-reporting) | the re-aged STAGE, AGE_BAND and ROUTE values of a period with X-Data-As-Of; a 422 on a reversed period and a 403 without Reporting R | APP, gateway-bff, contract tests |
| gateway-bff route fake | the merged SCR-37 answer with the reported values read once | APP, contract tests |

Each fake is generated from its document, versioned with the baseline and replaced by its owner in SIT without a change to a consumer.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 1 consumed | the measure read on `/api/recovery/reporting/v1`; the rule-version read of rwb-decision; one hop, 2 s |
| Kafka | none published, 4 consumed | EV-01, EV-05, EV-30 and the upstream reclassification fact; the change record leaves on `rwb.decision-record.v1` through the library |
| Temporal | none | the step runs inside JOB-15 and the event handler |
| File | none | no file is declared or consumed |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.reporting.contract`; artefacts under `contracts/rwb-reporting/`: `openapi-v1.yaml` (increment), `consumed.yaml`, `subscriptions.yaml`, `record.yaml`, `messages.yaml`, `fakes/*.json`.

| Component | Type | Responsibility |
|---|---|---|
| `openapi-v1.yaml` | Document | the one read, its parameters, its answer members, its dimension description and its errors |
| `consumed.yaml` | Document | the rule-version declaration, its placeholder and its review state |
| `subscriptions.yaml` | Document | the four subscriptions, their consumer groups and their envelope rule |
| `record.yaml` | Document | the change record element on the shared topic |
| `messages.yaml` | Document | the message map of section 14 |
| `fakes/` | Generator | the five fakes, generated from the documents and versioned with them |
| `ContractTag` | Build step | tags the baseline and hands the tag to the app story |

**Build steps.** (1) Write the OpenAPI increment and lint it; test AC1 and AC2. (2) Write the shape statement and pass the negative-shape test; test AC3. (3) Write the four subscriptions and the record element; test AC4 and AC5. (4) Generate the fakes and run the drift test; test AC6. (5) Tag `v1`, publish the tag and the sign-off note; test AC7.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | the local record library and the topic `rwb.decision-record.v1`; the record element of this key | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/reporting/v1`; the one read and its dimension semantics | none |
| DP-19 | Screen, ace-web | the gateway-bff composite route the read is served through | H RWB-PLT-N001-CON |

### 14. Validation and messages

| ID | When | Status and code |
|---|---|---|
| MSG-P1-001 | A data product behind the case facts is stale | 503 on a read of stale data; the text carries the product and the date |
| MSG-P7-003 | The change record cannot be written | 500 on the operation; the text says nothing was changed |
| MSG-P4-002 | The role lacks Reporting R | 403 on the operation; nothing changes |
| MSG-GEN-001 | A field is missing on a request | 400 with the field name |
| MSG-GEN-003 | A period has `from` after `to` | 422 with the two field names and no value |
| MSG-GEN-006 | The rule read or another named system is unavailable | 503 with the system name only |
| MSG-P3-027 | No rule version is in force on the business date | 409 on a read with no version; the text is the rule owner's |

The envelope of every error is the platform problem shape with `type`, `title`, `status`, `detail`, `instance` and `traceId`, and carries no personal data. The six business texts are the legacy texts of RWB-E8-002 section 14, the FSD P9 VR-P9-010-1 text and the rule owner's text, copied unchanged.

### 15. Screens and states

The legacy story has no screen, and this baseline serves none of its own: the re-aged classification is read on SCR-37 Steering dashboard through the gateway-bff composite route of RWB-PLT-N001-CON (DP-19). The baseline therefore declares the read that fills the screen and the states the reader sees — reported, re-aged, stale and held as the app story lists them — and declares no screen, no fragment and no field of its own.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P9-E8002-CON-01 | AC1 | Contract | the OpenAPI increment validated and compared with the ownership rows |
| TC-P9-E8002-CON-02 | AC2 | Contract | the dimension description and the examples linted for a frozen stage, band or threshold |
| TC-P9-E8002-CON-03 | AC3 | Contract | the shape statement compared with TSD P9 T3.1 and the ownership rows |
| TC-P9-E8002-CON-04 | AC4 | Contract | the four subscriptions with their groups, their envelope rule and the one placeholder |
| TC-P9-E8002-CON-05 | AC5 | Contract | the consumed declaration and the record element compared with the parents and the library |
| TC-P9-E8002-CON-06 | AC6 | Contract | the five fakes and their documented answers |
| TC-P9-E8002-CON-07 | AC7 | Contract | the tag `v1`, a proposed breaking change and the tag `v2` |

The seven are new with D-RCV-60 and test the baseline only; the four legacy cases of RWB-E8-002 stay with the criteria the app story owns. Integration copies of these IDs end in `-ITG`.

### 17. Guardrails

- No business value in a document, a fake or a test: the stages, routes, age bands, thresholds and measure codes are rows of their owners and appear here only as names.
- No personal data in a schema, a fixture or a log: references, codes, dates and counts only.
- No statement leaves `rwb_reporting`, no `v_ace_*` view is named, and no new table or column is declared for the classification.
- No declaration without a fake, no subscription without a consumer group and an envelope rule, no tag without the contract tests.
- The six message texts are copied, never reworded; a new text needs its owner.

### 18. Traceability

| Item | Value |
|---|---|
| Requirement and feature | FEAT-RPT-10 Classify, stage and re-age an account, Epic 8, module P9 (FSD P9 A2.10); the FSD "Requirements served" table is empty and the legacy story names no REQ, so the feature and the rules are the trace (GAP-2585; ASM-4280) |
| Business rules | BR-P9-010; VR-P9-010-1; NFR-065; R-UNI-22, R-UNI-38, R-UNI-39 |
| Legacy criteria | AC-P9-010-01 and AC-EXC-P9-010-01, AC-EXC-P9-010-02, owned by RWB-P9-E8002-APP |
| Legacy and disposition | RWB-E8-002, Split (rework); the contract slice owns no legacy criterion |
| Test cases | TC-P9-E8002-CON-01 to TC-P9-E8002-CON-07 |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-018, ADR-019, ADR-020, ADR-021, ADR-022 |

### 19. Out of scope

- The step, the projection, the write, the record and the read behaviour (RWB-P9-E8002-APP).
- The case-side recompute of the segment, the route reopen and the gate re-run of rule R-UNI-22, which stay with rwb-case (GAP-2586; ASM-4281).
- The rule rows, their authoring, test and promotion, and the rule package registry, which are rwb-decision's.
- The measure set and the `Measure` shape of RWB-E1-013, and the publish row and steering delta of RWB-E2-009, which stay with their parents RWB-P9-E1013-CON and RWB-P9-E2009-CON.
- The gateway-bff composite route itself and the screens it serves, which are the edge platform's.
- Any data lake, Power BI or file element, and any Schedule of this key.

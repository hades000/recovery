# RWB-P9-E8001-CON Produce regulatory returns

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P9-E8001-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-reporting |
| Service epic | RWB-SVC-P9 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-E8-001 |
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
| v1 | 22 November 2026 | D-RCV-60 realignment of RWB-E8-001 into rwb-reporting, contract slice | T3 Code / OpenCode / DeepSeek v4.1 Flash |

### 1. Story

As a **tech lead**, I want **the published contract baseline of the regulatory returns of rwb-reporting — the single provided read fixed under `/api/recovery/reporting/v1` with its closed answer, its definition version and its frozen flag, the consumed decision-log read of rwb-decision, the six consumed topics of the read model, the returns decision element on `rwb.decision-record.v1`, the negative declarations of the lake, the file and the event, the three owned tables and the three fakes**, so that **the app story of this legacy key builds against one fixed, testable contract on Day 1 and a return can never be published from a shape, a version or a source that nobody agreed**.

### 2. Business rationale

Contract-first REST with one hop is the decoupling decision (DP-13, ADR-020). The Ownership Map gives rwb-reporting one provided operation, GET `/reports/measures`, and three tables; the TSD P9 endpoint inventory has the same single row, API-P9-001. The baseline therefore fixes that one operation and nothing else: no second path is invented for a return, because a second path would be a second owner of the same measure and the same answer.

What the baseline must fix for the return is narrower and sharper than a path. A measure is only defensible if the answer says which definition produced it, so the answer carries `definition_version`, `business_date`, the product group, the dimension and the `frozen` flag; the returns decision on the shared `rwb.decision-record.v1` carries the rule version in force (DP-03), which is what the legacy AC1 records. The baseline also fixes, in the negative, what the return must never be again: no data lake copy, no INT-19 extract file, no event of this service and no second Schedule, because Architecture v5 removes the lake (DP-17, ADR-018) and the pattern set of this key carries neither DP-09 nor DP-10.

The contested points are carried as gaps and assumptions rather than settled quietly: the return layout and the field types beyond the TSD P9 T3.1 definitions are unset, the query parameters beyond the five of T-A.2 are additive guesses, the consumed event names beyond `rwb.case.CaseStateChanged.v1` are catalogue work, the decision code is unnamed, the texts of MSG-P9-002 and MSG-P9-003 do not exist, the data lake removal conflicts with the FSD A2.7.2 and TSD P9 T5.1 as written, and the plan declares no C row for the decision-log read.

### 3. Preconditions

- The service template and the naming library are in force, so the base, the schema, the topic and the queue follow the platform rule and not a local choice (RWB-PLT-TPL).
- The platform error envelope, the CloudEvents 1.0 envelope and the retry and `.dlt` topic convention are the platform baseline (RWB-PLT-EVT, RWB-PLT-TE006-CON); this document narrows them and never redefines them.
- The decision-record library of DP-03 and its topic `rwb.decision-record.v1` are available as a platform contract (RWB-PLT-E1027-CON).
- The operations and tables of section 12 are taken from the Ownership Map only: `measure_definition`, `measure_snapshot` and `measure_publish` are rwb-reporting's, the decision ledger is rwb-decision's, the case is rwb-case's and the documents are rwb-document's.
- The decision-log read of rwb-decision has no C row in the plan of this key; it is declared as consumed and faked (GAP-2583; ASM-4272).
- No build dependency: a CON story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the additive change to the rwb-reporting OpenAPI 3.1 document: the measure read of API-P9-001, its five query parameters, its 200 answer, its four error responses and its access right.
2. Fix the answer as a closed set: `measureCode`, `name`, `definitionVersion`, `businessDate`, `productGroup`, `dimensionCode`, `dimensionValue`, `value`, `caseCount`, `unit` and `frozen`, with no definition text, no formula and no free-text label.
3. Fix the fact that the return set is read through this one operation, and record that no second path is declared because the Ownership Map gives rwb-reporting one provided operation.
4. Record the consumed decision-log read of rwb-decision as consumed, one hop and faked, with the members the return needs.
5. Record the six consumed owner topics and the dedupe rule, and stress that event names beyond `rwb.case.CaseStateChanged.v1` are catalogue work.
6. Record the decision element: decision reference FEAT-RPT-07, the rule version in force, the business date, the definition version, the result PUBLISHED or HELD, through the local library on the shared topic.
7. Record the negative declarations: no event of this service, no domain workflow, no file, no data lake copy, no second base, no second Schedule.
8. Record the three owned tables as shapes: measure definition, frozen snapshot, publish row, with the unique keys of TSD P9 T3.1.
9. Publish the three fakes, the eight contract tests, the baseline tag and the sign-off note to RWB-P9-E8001-APP.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the envelope | The platform schema message | AC1 |
| X2 | A member is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC2 |
| X3 | The answer carries a formula, a definition text or a personal field | The closed-set test fails the build | None | AC2 |
| X4 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC7 |
| X5 | An event of rwb-reporting is declared, or the document declares a lake path | The absence test fails the build | None | AC6 |
| X6 | The document declares another service's operation as provided | The review fails the baseline; the operation is described as consumed and faked | None | AC5 |
| X7 | The answer quotes a rule version as a constant | The decision-element test fails; the version is a value of the record | None | AC3 |
| X8 | The Schedule of JOB-15 is restated with a name no source gives | The row carries the placeholder and the platform owns the registration | None | AC8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the ownership rows and the naming rule only |
| Negotiable | The member names beyond the TSD fields, the paging and the decision code are settled with the rwb-decision, gateway-bff and reporting owners; the base and the topic are fixed by the target |
| Valuable | Unblocks the app story on Day 1 and stops the return from ever being published from an unversioned or unspecified shape |
| Estimable | One document change, one event element, one decision element, nine contract tables, three fakes and eight contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact and not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the regulatory returns of rwb-reporting

  Background:
    Given the service naming rule of the platform library is in force
    Given the base of rwb-reporting is /api/recovery/reporting/v1 and its schema is rwb_reporting
    Given the ownership map gives rwb-reporting one provided operation and three tables

  Scenario: AC1 The one provided operation is declared and validates (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-reporting is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares GET /reports/measures under the base /api/recovery/reporting/v1, owned by rwb-reporting, with the query parameters measure, product, route, from and to
    Then the operation declares capability area Reporting with right R and scope applied
    Then it declares the responses 200, 401, 403 and 503 with one envelope and one message ID per condition
    Then it declares no other path as provided, and API-P9-001 is the only row it adds to the P9 inventory

  Scenario: AC2 The measure answer is a closed set that carries its version (new, D-RCV-60)
    Given the Measure answer of the baseline
    When its members are compared with the ownership map and TSD P9 T3.1
    Then a row carries measureCode, name, definitionVersion, businessDate, productGroup, dimensionCode, dimensionValue, value, caseCount, unit and frozen
    Then definitionVersion is a string of twenty characters and frozen is a boolean
    Then the answer carries no formula, no definition text, no approved by and no free-text label
    Then the member names beyond the TSD P9 fields and the page limits are Not specified in the source documents (GAP-2583; ASM-4271) and the document marks them so
    Then a build that adds a formula or a definition text to the answer fails the closed-set test

  Scenario: AC3 The returns decision element is fixed with its rule version (new, D-RCV-60)
    Given the decision element of the baseline
    When it is compared with the decision-record library and the legacy AC1
    Then the element declares the decision reference FEAT-RPT-07, the rule version in force, the business date, the definition version and the result PUBLISHED or HELD
    Then it is declared on the shared rwb.decision-record.v1 through the local library and never as an event of this service
    Then no rule version, no definition version and no measure value is a contract constant
    Then a refused write blocks the return and raises the incident of R-UNI-39
    Then the decision code is Not specified in the source documents (GAP-2583; ASM-4265) and the document carries the placeholder

  Scenario: AC4 The consumed facts are declared and this service publishes no event (new, D-RCV-60)
    Given the event section of the baseline
    When it is compared with the event catalogue and the connection matrix
    Then rwb.case.CaseStateChanged.v1 is declared as consumed, event 05 on rwb.case.events.v1, owner P3 rwb-case, keyed by caseId
    Then the facts of rwb-comms, rwb-treatment, rwb-debtsale, rwb-writeoff and rwb-payment are declared as consumed on their own topics
    Then the event names beyond rwb.case.CaseStateChanged.v1 are Not specified in the source documents (GAP-2583; ASM-4273) and the document names the topics only
    Then the document declares no published event of rwb-reporting and no second topic for this capability
    Then the dedupe rule by the CloudEvents id and the inbox is declared

  Scenario: AC5 The three tables are the only owned tables and no cross-schema read is declared (new, D-RCV-60)
    Given the tables of the baseline
    When they are compared with the ownership map
    Then measure_definition, measure_snapshot and measure_publish are declared as rwb_reporting tables with their field ranges DF-RPT-031 to DF-RPT-058
    Then decision_log_entry, recovery_case, document and rule rows are named as other owners' and consumed only through their contracts
    Then the document declares no view of this service, no v_ace_ view and no shared login
    Then the operation declares no join and no query against another schema, and a static check fails a build that adds one

  Scenario: AC6 No lake, no file and no second base is declared (new, D-RCV-60)
    Given the document, the tables and the call-type summary of the baseline
    When they are reviewed against Architecture v5
    Then no data lake path, no INT-19 extract file and no Power BI copy is declared or consumed
    Then the file call type is None and the baseline states that the return is read from the frozen snapshots of this schema
    Then the conflict between the FSD A2.7.2 and TSD P9 T5.1, which still name Power BI and the data lake, and Architecture v5 is recorded once with the assumed replacement
    Then the absence test fails a build that declares a lake path or a file

  Scenario: AC7 The three contract fakes answer the document (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the operation or the element it serves
    Then the rwb-decision fake answers the decision facts of a date, an empty day, a refused write and an answer beyond the budget
    Then the decision-record library stub answers an accepted record with the rule version and a stopped chain
    Then the event harness answers one synthetic business date, a repeat delivery with the same CloudEvents id and a stale product
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC8 The nine tables are complete, the job row is fixed and the baseline is signed off (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the ownership map, with None where the element is empty
    Then 12.6 names JOB-15 of rwb-reporting at 01:30 and declares no second Schedule and no Quartz row
    Then the call-type summary declares one operation provided, one consumed, no event published, six topics consumed and no file
    Then the baseline is tagged and the app story has accepted it
```

These eight criteria are new for the contract baseline and test the artefact only; the legacy criteria AC1 and AC2 of RWB-E8-001 are owned by RWB-P9-E8001-APP and none of them is copied here.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/reporting/v1`; the document never declares another service's path as provided | DP-13; Template and Rules §R4 |
| BR2 | The topic is `rwb.reporting.events.v1` and an event name would be `rwb.reporting.<Event>.v1`; this service owns no event | DP-14; Ownership Map |
| BR3 | Every consumed event carries the CloudEvents 1.0 envelope, is keyed by caseId and carries no personal data | Architecture v5 event notes |
| BR4 | A read declares no Idempotency-Key and no request body; this baseline has no POST of its own | Platform baseline |
| BR5 | Error responses use one envelope and one message ID per condition; the legacy texts stay unchanged | Template and Rules §R7.2 s14 |
| BR6 | A schema change is additive within major version 1; a breaking change is a new major version | Architecture v5 API notes |
| BR7 | The document lists only operations and tables owned by rwb-reporting | Ownership Map |
| BR8 | No value a business person may change is a contract constant: measures, formulas, units, data products, dimensions and definition versions are data rows | BR-P9-007 |
| BR9 | The decision record is the local library's entry on the shared `rwb.decision-record.v1`, never an event of this service | DP-03 |
| BR10 | The data lake and Power BI copy is removed; the return is read from the frozen snapshots of this schema | DP-17; ADR-018 (GAP-2584) |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The operation, the closed answer, the decision element, the negatives and the tables are described | In review |
| In review | Consumer sign-off | The app story and the rwb-decision, gateway-bff and platform owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A member is added within major version 1, for example a data product filter | Baselined |
| Baselined | Breaking change | A member is removed, renamed or retyped | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A lake path, a file or a published event appears | The absence test of AC6 fails | In review |

The snapshot and publish states of section 9 of the app story are the app story's; this baseline fixes the shapes and moves nothing.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-reporting | Owns the OpenAPI document and the fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, the lake removal and the correction of the ownership rows the baseline consumes |
| Consuming teams (app story, rwb-decision, gateway-bff, platform library) | Review and sign off the parts they consume |
| Platform library owner | Owns the CloudEvents envelope, the error envelope, the naming rule and the decision library |
| Data steward | Confirms that no personal data field and no formula is declared in the answer or in an event |

The per-service login name behind the security scheme is not part of this baseline; the document names the scheme "the rwb-reporting login (DP-02)".

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Measure answer | `measureCode` DF-RPT-032, `name` DF-RPT-033, `definitionVersion` DF-RPT-037, `businessDate` DF-RPT-044, `productGroup` DF-RPT-045, `dimensionCode` DF-RPT-046, `dimensionValue` DF-RPT-047, `value` DF-RPT-048, `caseCount` DF-RPT-049, `unit` DF-RPT-036, `frozen` DF-RPT-051 |
| Publish element | `businessDate` DF-RPT-054, `status` DF-RPT-055 with PUBLISHED or HELD, `caseListCount` DF-RPT-056, `dashboardCount` DF-RPT-057, `heldReason` DF-RPT-058 |
| Decision element | FEAT-RPT-07 as the decision reference, the rule version in force, the business date, the definition version, the result PUBLISHED or HELD, decided at; DF-DEC-001 to DF-DEC-018 |
| Consumed facts | `caseId` and the decision facts of a date, from the rwb-decision read and the six topics; codes, dates, amounts and counts only |
| Not declared | Any formula, definition text, approved by, personal field, lake path or file (GAP-2583; ASM-4271) |

The field types and required flags of the answer beyond TSD P9 T3.1, the page limits and the optional dimension filter are settled in the baseline review (GAP-2583; ASM-4274).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-reporting (P9); base `/api/recovery/reporting/v1`.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/reports/measures` | Measure[] of status 200 out: the members of section 11 for the frozen rows of a period, filtered by measure, product, route, from and to | Reporting, right R, scope applied | Not applicable |

The operation answers 401, 403 and 503 with the error envelope and one message ID of section 14; TSD P9 T-A.2 fixes the request, the answer and the three errors. It is the only provided operation of the baseline, because the Ownership Map gives rwb-reporting one (GAP-2583; ASM-4270).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| GET | the decision-log read of `/api/recovery/decision/v1` | P7 rwb-decision | The decision facts and the rule version of a business date, faked. The plan declares no C row for it (GAP-2583; ASM-4272) |

One row, one hop, on the owner's published contract; no row reads a table or a view of another service, and the document declares no other consumed operation.

#### 12.3 Events published

None. The Ownership Map gives rwb-reporting no event; the returns record is relayed on the shared `rwb.decision-record.v1` by the local library of DP-03 and never as an event of this service.

#### 12.4 Events consumed

| Event | Topic | Owner | Consumer contract element |
|---|---|---|---|
| `rwb.case.CaseStateChanged.v1` (event 05) | `rwb.case.events.v1` | P3 rwb-case | caseId, fromState, toState, changedAt, behind the count measures; dedupe by the CloudEvents id |
| The notice and contact facts | `rwb.comms.events.v1` | P6 rwb-comms | The notice and contact measures |
| The treatment outcome facts | `rwb.treatment.events.v1` | S2 rwb-treatment | The settlement and restructuring measures |
| The debt-sale lot facts | `rwb.debtsale.events.v1` | S6 rwb-debtsale | The sale measures |
| The write-off and recovery facts | `rwb.writeoff.events.v1` | S7 rwb-writeoff | The write-off and recovery measures |
| The payment facts | `rwb.payment.events.v1` | P8 rwb-payment | The cash and recovery measures |

The connection matrix names rwb-reporting as a listener on exactly these six owners, so the rows are not a new claim. The event names beyond the first are Not specified in the sources read for this WP and are pinned by the Kafka Topic and Event Catalog (GAP-2583; ASM-4273).

#### 12.5 Workflows and activities

None. The Ownership Map gives rwb-reporting no workflow; the return runs as the step of JOB-15 of section 12.6 inside the service's own run, and the baseline declares no child workflow, no activity contract and no Nexus call.

#### 12.6 Schedules

| Job | Queue | When | Contract element |
|---|---|---|---|
| JOB-15, the daily reporting run of rwb-reporting | `rwb-reporting` | Daily at 01:30 | The returns step of the app story; the baseline declares no second Schedule, no Quartz row and no shared job table |

The Schedule name and the registration detail are the platform's and are Not specified in the sources read for this WP (GAP-2583; ASM-4276).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| measure_definition | P9 (rwb_reporting) | The definition in force: measure code, name, formula as data, data product, unit, definition version, valid from |
| measure_snapshot | P9 (rwb_reporting) | The value per measure, definition version, business date, product group, dimension and the frozen flag |
| measure_publish | P9 (rwb_reporting) | The PUBLISHED or HELD status of a business date with the two counts and the held reason |

`decision_log_entry` is P7 rwb-decision's, `recovery_case` is P3 rwb-case's, `document` is P5 rwb-document's and the ACE views are P1's; the document names them only as consumed answers (DP-01). No table of `rwb_reporting` carries a formula string as a contract constant, a definition text or a personal field (AC2).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-decision WireMock | The decision facts of a date, an empty day, a refused write and an answer beyond the budget; the path and the members are fixed with the P7 owner (GAP-2583; ASM-4272) | App story, contract tests |
| decision-record library stub | An accepted record carrying the rule version and a stopped chain | App story, contract tests |
| event harness | One synthetic business date across the six topics, a repeat delivery with the same CloudEvents id and a stale product | App story, contract tests |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 1 consumed | The measure read provided; the decision-log read of P7 consumed; one hop each |
| Kafka | None declared as published, 6 topics declared as consumed | The read model of the day; the decision record is the library's on the shared topic |
| Temporal | The job's own run | JOB-15 on `rwb-reporting`; no workflow of this key |
| File | None | No file and no lake path is declared (GAP-2584; ASM-4275) |

### 13. Solution plan

**Deliverables.** The additive change to `openapi/rwb-reporting-v1.yaml` for the measure read and its closed answer, the AsyncAPI note naming the six consumed topics and no published event, the contract README rows for the decision element and the negatives, and the three WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/reporting/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-01 is applied as a prohibition and adds no dependency: the decision facts arrive on the owner's contract. DP-17 is not in the pattern set of this key and adds no dependency; the lake removal it states is recorded once as a conflict and an assumption.

**Build steps**

1. Add the measure read and the closed answer of AC2 to the OpenAPI document and validate the closed-set rule in the pipeline.
2. Record the decision-log read of AC5 and the six consumed topics of AC4, and validate the AsyncAPI note against the registry.
3. Record the decision element of AC3 with the placeholder on the decision code and the rule version.
4. Record the negatives of AC6 and write the absence test for a lake path, a file, an event and a second base.
5. Record the three tables of AC8 with the unique keys of TSD P9 T3.1.
6. Publish the three fakes and the eight contract tests; a drift between a fake and the document fails the build.
7. Baseline tag and the sign-off note, including the app story and the rwb-decision, gateway-bff and platform owners.

**Done when** the OpenAPI and AsyncAPI artefacts validate in the pipeline, the eight contract tests pass, the three fakes answer every consumed path, the drift test is green and the app story has accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | The role lacks the Reporting right | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The returns decision record could not be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | A data product is stale at the read boundary | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-GEN-006 | A downstream does not answer within the budget | {system} is not available. Your request is queued and will be retried. |
| MSG-P9-002 | The counts behind a publish do not match | Not specified in the source documents (GAP-2583; ASM-4266) |
| MSG-P9-003 | A measure has no definition in force | Not specified in the source documents (GAP-2583; ASM-4266) |

The schema-validation message of a failed body and the message of a consumed call that does not answer in time are the platform's own and are not redefined here. MSG-P7-003 and MSG-P4-002 are copied unchanged from the legacy story, which is the source of both texts.

### 15. Screens and states

The baseline serves the frozen measure set to SCR-37 Steering dashboard and to the reporting screens of the module through the gateway-bff composite route (DP-19); the screens, their states and their field masks belong to the story that owns each view and to RWB-PLT-N001-CON. The legacy story says there is no screen of its own, and none is declared here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E8-001-01 | AC1 | Component | A synthetic business date whose read answers the frozen set; the contract half answers the answer of AC2 and the decision of AC3 |
| TC-E8-001-02 | AC2 | Component | The decision record forced to refuse; the contract half answers the stopped chain of AC7 |
| TC-E8-001-03 | Access | Contract | RW-BIANAL reads in scope and a role without Reporting R is refused with MSG-P4-002; the contract half answers the 403 of AC1 |
| TC-E8-001-04 | Principle 5 | NFR | The decision record forced to fail on ten business dates; the contract half answers the stopped chain of AC7 |
| TC-P9-E8001-CON-01 | AC1 | Contract | The document validates; the one operation, its base, its five parameters, its access and its three errors are present |
| TC-P9-E8001-CON-02 | AC2 | Contract | The answer validates with eleven members; no formula, no definition text and no personal field |
| TC-P9-E8001-CON-03 | AC3 | Contract | The decision element carries FEAT-RPT-07, the rule version, the business date, the definition version and the two results |
| TC-P9-E8001-CON-04 | AC4 | Contract | The six consumed topics validate against the registry; no published event of this service |
| TC-P9-E8001-CON-05 | AC5 | Contract | The three owned tables and the field ranges; no cross-schema read and no shared view |
| TC-P9-E8001-CON-06 | AC6 | Contract | The absence test: no lake path, no file, no Power BI copy and no second base |
| TC-P9-E8001-CON-07 | AC7 | Component | The three fakes match the document; a drifted fake fails the build |
| TC-P9-E8001-CON-08 | AC8 | Contract | The nine sub-tables present with owners; the JOB-15 row; the call-type counts |

The four legacy cases keep their legacy order and their legacy intent as the evidence the contract serves; the eight contract cases test the artefact and are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the contract: the measures, formulas, units, data products, dimensions, definition versions and the rule version stay data rows of their owners.
- No personal data in a schema, an example or a fake: case IDs, measure codes, codes, dates, amounts and counts only.
- The contract names only rwb-reporting tables and only the one operation owned by rwb-reporting; the decision-log read is consumed and faked, never declared as provided (DP-01).
- One base, one topic and one queue per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- No retired element is introduced: the absence test fails a build that declares a lake path, an INT-19 file, a Quartz row or a published event.
- Every example in the document is synthetic; no production payload is copied into a schema or a fake.
- The error envelope, the CloudEvents envelope and the naming rule come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| FEAT-RPT-07 | Produce regulatory returns from the data products and the decision log | The measure read, the closed answer and the decision element | TC-P9-E8001-CON-01, TC-P9-E8001-CON-02, TC-P9-E8001-CON-03 |
| BR-P9-007 | No value a business person may change is written in code | The closed answer and the data rows behind it | TC-P9-E8001-CON-02 |
| VR-P9-007-1 | A stale data product holds the return | The MSG-P1-001 row of 14 and the negative on a copied product | TC-P9-E8001-CON-01 |
| NFR-065 | Business measures per decision come from the decision log | The decision-log read of 12.2 and the decision element of 12.3 | TC-P9-E8001-CON-03, TC-P9-E8001-CON-04 |
| R-UNI-39 | A decision record that cannot be written blocks the action | The refused-write case of the decision element | TC-P9-E8001-CON-03, TC-P9-E8001-CON-07 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E8-001, disposition Split (rework) |
| Legacy criteria | AC1 and AC2 of the legacy story, both owned by RWB-P9-E8001-APP; this baseline copies neither |
| Test cases | The four legacy cases as the evidence the contract serves, and the eight new contract cases TC-P9-E8001-CON-01 to -08 |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-018, ADR-019, ADR-020, ADR-021, ADR-022 |

### 19. Out of scope

- The implementation of the returns run, the freeze, the publish row and the read (RWB-P9-E8001-APP).
- The measure definitions, their formulas, units and data products, and the approval of a definition version (RW-DATASTEW, the administration screens of the module).
- The baseline measure set, the steering dashboard data set, the benefit tracking and the reconciliation of the case counts of the same service: projected, not redefined.
- The classification, staging and re-ageing capability of the same epic (FEAT-RPT-10, RWB-E8-002).
- The decision ledger, its schema and its own read contract (P7 rwb-decision): consumed and faked.
- The delivery of an extract to a regulator, the data lake and Power BI (INT-19 and INT-20 removed; GAP-2584).
- The registration, cron and runbook of JOB-15's Schedule, and the deployment, dashboards and alerts of this capability.
